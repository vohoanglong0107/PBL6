# -*- coding: utf-8 -*-
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
""" generate.py """
import os

import numpy as np
import tensorflow as tf

from app.dataset import Dataset
from app.model import get_fingerprinter, get_melspec_layer
from app.utils import load_checkpoint, logging_tqdm
from loguru import logger


def build_fp(cfg):
    """Build fingerprinter"""
    # m_pre: log-power-Mel-spectrogram layer, S.
    m_pre = get_melspec_layer(cfg, trainable=False)

    # m_fp: fingerprinter g(f(.)).
    m_fp = get_fingerprinter(cfg, trainable=False)
    return m_pre, m_fp


def get_data_source(cfg, source_root_dir):
    dataset = Dataset(cfg)
    return dataset.get_custom_db_ds(source_root_dir)


@tf.function
def test_step(X, m_pre, m_fp):
    """Test step used for generating fingerprint"""
    # X is not (Xa, Xp) here. The second element is reduced now.
    m_fp.trainable = False
    return m_fp(m_pre(X))  # (BSZ, Dim)


def generate_fingerprint(
    cfg,
    source_root_dir,
    output_root_dir,
    checkpoint_uri=None,
):
    # Build and load checkpoint
    m_pre, m_fp = build_fp(cfg)
    load_checkpoint(m_fp, checkpoint_uri)

    # Get data source
    ds = get_data_source(cfg, source_root_dir)
    os.makedirs(output_root_dir, exist_ok=True)

    # Generate
    bsz = int(cfg["BSZ"]["TS_BATCH_SZ"])  # Do not use ds.bsz here.
    # n_items = len(ds) * bsz
    n_items = ds.n_samples
    dim = cfg["MODEL"]["EMB_SZ"]
    """
    Why use "memmap"?
    • First, we need to store a huge uncompressed embedding vectors until
      constructing a compressed DB with IVF-PQ (using FAISS). Handling a
      huge ndarray is not a memory-safe way: "memmap" consume 0 memory.
    • Second, Faiss-GPU does not support reconstruction of DB from
      compressed DB (index). In eval/eval_faiss.py, we need uncompressed
      vectors to calaulate sequence-level matching score. The created
      "memmap" will be reused at that point.
    Reference:
        https://numpy.org/doc/stable/reference/generated/numpy.memmap.html
    """
    # Create memmap, and save shapes
    assert n_items > 0
    arr_shape = (n_items, dim)
    arr = np.memmap(
        f"{output_root_dir}/db.mm", dtype="float32", mode="w+", shape=arr_shape
    )
    np.save(f"{output_root_dir}/db_shape.npy", arr_shape)
    songs = []

    # Fingerprinting loop
    logger.info(
        "=== Generating fingerprint from \x1b[1;32m'db'\x1b[0m "
        + f"bsz={bsz}, {n_items} items, d={dim}"
        + " ==="
    )

    with logging_tqdm(
        total=len(ds), postfix=["tr loss", dict(value=0)], mininterval=30
    ) as tqdm:

        i = 0
        while i < len(ds):
            X, _, song = ds[i]
            songs = songs + song
            emb = test_step(X, m_pre, m_fp)
            arr[i * bsz : (i + 1) * bsz, :] = emb.numpy()  # Writing on disk.
            tqdm.update(1)
            i += 1

    logger.info(
        f"=== Succesfully stored {arr_shape[0]} fingerprint to {output_root_dir} ==="
    )

    arr.flush()
    del arr  # Close memmap
    np.savetxt(f"{output_root_dir}/songs.txt", songs, delimiter=";", fmt="%s")
