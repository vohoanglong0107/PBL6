# -*- coding: utf-8 -*-
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
""" trainer.py """
import tensorflow as tf

from app.dataset import Dataset
from app.model import get_fingerprinter, get_melspec_layer
from app.utils import logging_tqdm
from loguru import logger
from tensorflow.keras.optimizers import Adam

from .agumentation_pipeline import get_specaug_chain_layer
from .experiment_helper import ExperimentHelper
from .mini_search_subroutines import mini_search_eval
from .NTxentLoss import NTxentLoss


def build_fp(cfg):
    """Build fingerprinter"""
    # m_pre: log-power-Mel-spectrogram layer, S.
    m_pre = get_melspec_layer(cfg, trainable=False)

    # m_specaug: spec-augmentation layer.
    m_specaug = get_specaug_chain_layer(cfg, trainable=False)
    assert m_specaug.bypass is False  # Detachable by setting m_specaug.bypass.

    # m_fp: fingerprinter g(f(.)).
    m_fp = get_fingerprinter(cfg, trainable=False)
    return m_pre, m_specaug, m_fp


@tf.function
def train_step(X, m_pre, m_specaug, m_fp, loss_obj, helper):
    """Train step"""
    # X: (Xa, Xp)
    # Xa: anchors or originals, s.t. [xa_0, xa_1,...]
    # Xp: augmented replicas, s.t. [xp_0, xp_1] with xp_n = rand_aug(xa_n).
    n_anchors = len(X[0])
    X = tf.concat(X, axis=0)
    feat = m_specaug(m_pre(X))  # (nA+nP, F, T, 1)
    m_fp.trainable = True
    with tf.GradientTape() as t:
        emb = m_fp(feat)  # (BSZ, Dim)
        loss, sim_mtx, _ = loss_obj.compute_loss(
            emb[:n_anchors, :], emb[n_anchors:, :]
        )  # {emb_org, emb_rep}
    g = t.gradient(loss, m_fp.trainable_variables)
    helper.optimizer.apply_gradients(zip(g, m_fp.trainable_variables))
    return loss, sim_mtx


@tf.function
def val_step(X, m_pre, m_fp, loss_obj):
    """Validation step"""
    n_anchors = len(X[0])
    X = tf.concat(X, axis=0)
    feat = m_pre(X)  # (nA+nP, F, T, 1)
    m_fp.trainable = False
    emb = m_fp(feat)  # (BSZ, Dim)
    loss, sim_mtx, _ = loss_obj.compute_loss(
        emb[:n_anchors, :], emb[n_anchors:, :]
    )  # {emb_org, emb_rep}
    return loss, sim_mtx


@tf.function
def test_step(X, m_pre, m_fp):
    """Test step used for mini-search-validation"""
    X = tf.concat(X, axis=0)
    feat = m_pre(X)  # (nA+nP, F, T, 1)
    m_fp.trainable = False
    emb_f = m_fp.front_conv(feat)  # (BSZ, Dim)
    emb_f_postL2 = tf.math.l2_normalize(emb_f, axis=1)
    emb_gf = m_fp.div_enc(emb_f)
    emb_gf = tf.math.l2_normalize(emb_gf, axis=1)
    return emb_f, emb_f_postL2, emb_gf  # f(.), L2(f(.)), L2(g(f(.))


def mini_search_validation(
    ds, m_pre, m_fp, mode="argmin", scopes=[1, 3, 5, 9, 11, 19], max_n_samples=3000
):
    """Mini-search-validation"""
    # Construct mini-DB
    key_strs = ["g(f)"]
    m_fp.trainable = False
    (db, query, emb, dim) = (dict(), dict(), dict(), dict())
    dim["g(f)"] = m_fp.emb_sz
    bsz = ds.bsz
    n_anchor = bsz // 2
    n_iter = min(len(ds), max_n_samples // bsz)
    for k in key_strs:
        (db[k], query[k]) = (tf.zeros((0, dim[k])), tf.zeros((0, dim[k])))
    for i in range(n_iter):
        X = ds.__getitem__(i)
        _, _, emb["g(f)"] = test_step(X, m_pre, m_fp)

        for k in key_strs:
            db[k] = tf.concat((db[k], emb[k][:n_anchor, :]), axis=0)
            query[k] = tf.concat((query[k], emb[k][n_anchor:, :]), axis=0)

    # Search test
    accs_by_scope = dict()
    for k in key_strs:
        tf.print(
            f"======= mini-search-validation: \033[31m{mode} \033[33m{k} \033[0m======="
            + "\033[0m"
        )
        query[k] = tf.expand_dims(query[k], axis=1)  # (nQ, d) --> (nQ, 1, d)
        accs_by_scope[k], _ = mini_search_eval(
            query[k], db[k], scopes, mode, display=True
        )
    return accs_by_scope, scopes, key_strs


def trainer(cfg, checkpoint_name):
    dataset = Dataset(cfg)

    # Build models.
    m_pre, m_specaug, m_fp = build_fp(cfg)

    # Learning schedule
    total_nsteps = cfg["TRAIN"]["MAX_EPOCH"] * len(dataset.get_train_ds())
    if cfg["TRAIN"]["LR_SCHEDULE"].upper() == "COS":
        lr_schedule = tf.keras.experimental.CosineDecay(
            initial_learning_rate=float(cfg["TRAIN"]["LR"]),
            decay_steps=total_nsteps,
            alpha=1e-06,
        )
    elif cfg["TRAIN"]["LR_SCHEDULE"].upper() == "COS-RESTART":
        lr_schedule = tf.keras.experimental.CosineDecayRestarts(
            initial_learning_rate=float(cfg["TRAIN"]["LR"]),
            first_decay_steps=int(total_nsteps * 0.1),
            num_periods=0.5,
            alpha=2e-06,
        )
    else:
        lr_schedule = float(cfg["TRAIN"]["LR"])

    opt = Adam(learning_rate=lr_schedule)

    # Experiment helper: see utils.experiment_helper.py for details.
    with ExperimentHelper(
        checkpoint_name=checkpoint_name,
        optimizer=opt,
        model_to_checkpoint=m_fp,
        cfg=cfg,
    ) as helper:
        loss_obj = NTxentLoss(tau=cfg["LOSS"]["TAU"])

        # Training loop
        ep_start = helper.epoch
        ep_max = cfg["TRAIN"]["MAX_EPOCH"]
        for ep in range(ep_start, ep_max + 1):
            logger.info(f"EPOCH: {ep}/{ep_max}")

            # Train
            max_train_items = cfg["TRAIN"]["MAX_NUM_ITEMS"]
            train_ds = dataset.get_train_ds(max_train_items=max_train_items)
            with logging_tqdm(total=len(train_ds), mininterval=300) as tqdm:
                i = 0
                while i < len(train_ds):
                    X = train_ds[i]  # X: Tuple(Xa, Xp)
                    loss, sim_mtx = train_step(
                        X, m_pre, m_specaug, m_fp, loss_obj, helper
                    )
                    avg_loss = helper.update_tr_loss(loss)

                    tqdm.set_postfix({"tr loss": float(avg_loss)})
                    tqdm.update(1)
                    i += 1

            if cfg["TRAIN"]["SAVE_IMG"] and (sim_mtx is not None):
                helper.write_image_tensorboard("tr_sim_mtx", sim_mtx.numpy())

            # Validate
            val_ds = dataset.get_val_ds(max_song=250)  # max 500
            with logging_tqdm(total=len(val_ds), mininterval=30) as tqdm:
                i = 0
                while i < len(val_ds):
                    X = val_ds[i]  # X: Tuple(Xa, Xp)
                    loss, sim_mtx = val_step(X, m_pre, m_fp, loss_obj)
                    avg_loss = helper.update_val_loss(loss)
                    tqdm.set_postfix({"val loss": float(avg_loss)})
                    tqdm.update(1)
                    i += 1

            if cfg["TRAIN"]["SAVE_IMG"] and (sim_mtx is not None):
                helper.write_image_tensorboard("val_sim_mtx", sim_mtx.numpy())

            # On epoch end
            helper.update_on_epoch_end(save_checkpoint_now=True)

            # Mini-search-validation (optional)
            if cfg["TRAIN"]["MINI_TEST_IN_TRAIN"]:
                accs_by_scope, scopes, key_strs = mini_search_validation(
                    val_ds, m_pre, m_fp
                )
                for k in key_strs:
                    helper.update_minitest_acc(accs_by_scope[k], scopes, k)
