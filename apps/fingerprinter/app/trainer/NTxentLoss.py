import tensorflow as tf


class NTxentLoss:
    def __init__(self, tau=0.05, **kwargs):
        """Init."""
        self.tau = tau

    @tf.function
    def drop_diag(self, x, mask_not_diag, n_org):
        x = tf.boolean_mask(x, mask_not_diag)
        return tf.reshape(x, (n_org, n_org - 1))

    @tf.function
    def compute_loss(self, emb_org, emb_rep):
        """NTxent Loss function for neural audio fingerprint.

        • Every input embeddings must be L2-normalized...
        • Batch-size must be an even number.

        Args
        ----
        emb_org: tensor of shape (nO, d)
            nO is the number of original samples. d is dimension of embeddings.
        emb_rep: tensor of shape (nR, d)
            nR is the number of replica (=augmented) samples.

        Returns
        -------
            (loss, sim_mtx, labels)

        """
        n_org = len(emb_org)
        n_rep = len(emb_rep)
        assert len(emb_org) == len(emb_rep), f"{len(emb_org)} {len(emb_rep)}"
        labels = tf.one_hot(tf.range(n_org), n_org * 2 - 1)

        mask_not_diag = tf.cast(1 - tf.eye(n_org), tf.bool)
        ha, hb = emb_org, emb_rep  #
        logits_aa = tf.matmul(ha, ha, transpose_b=True) / self.tau
        logits_aa = self.drop_diag(logits_aa, mask_not_diag, n_org)  # modified
        logits_bb = tf.matmul(hb, hb, transpose_b=True) / self.tau
        logits_bb = self.drop_diag(logits_bb, mask_not_diag, n_org)  # modified
        logits_ab = tf.matmul(ha, hb, transpose_b=True) / self.tau
        logits_ba = tf.matmul(hb, ha, transpose_b=True) / self.tau
        categorical_cross_entropy_loss = tf.keras.losses.CategoricalCrossentropy(
            from_logits=True,
        )
        loss_a = categorical_cross_entropy_loss(
            labels, tf.concat([logits_ab, logits_aa], 1)
        )
        loss_b = categorical_cross_entropy_loss(
            labels, tf.concat([logits_ba, logits_bb], 1)
        )
        return loss_a + loss_b, tf.concat([logits_ab, logits_aa], 1), labels


# Unit-test
def test_loss():
    feat_dim = 5
    n_org = 3  # Batch-size N is 6
    n_rep = n_org
    tau = 0.05  # temperature
    emb_org = tf.random.uniform((n_org, feat_dim))  # this should be [org1, org2, org3]
    emb_rep = tf.random.uniform((n_rep, feat_dim))  # this should be [rep1, rep2, rep3]
    print(emb_org)
    print(emb_rep)

    loss_obj = NTxentLoss(tau=tau)
    loss, simmtx_upper_half, _ = loss_obj.compute_loss(emb_org, emb_rep)
    print(loss)
    print(simmtx_upper_half)
