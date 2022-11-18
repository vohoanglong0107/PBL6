import tensorflow as tf
from .config import read_config


def load_checkpoint(m_fp, checkpoint_uri=None):
    cfg = read_config()
    checkpoint_root_dir = cfg["DIR"]["LOG_ROOT_DIR"] + "downloaded-checkpoint/"
    if checkpoint_uri:
        import mlflow

        mlflow.artifacts.download_artifacts(
            checkpoint_uri,
            dst_path=checkpoint_root_dir,
        )
    """Load a trained fingerprinter"""
    # Create checkpoint
    checkpoint = tf.train.Checkpoint(model=m_fp)
    # because we save undef path = "checkpoint" with this
    # mlflow.log_artifacts(self._checkpoint_save_dir, artifact_path="checkpoint")
    checkpoint_dir = checkpoint_root_dir + "checkpoint/"
    c_manager = tf.train.CheckpointManager(checkpoint, checkpoint_dir, max_to_keep=None)

    # Load
    tf.print("\x1b[1;32mSearching for the latest checkpoint...\x1b[0m")
    latest_checkpoint = c_manager.latest_checkpoint
    if latest_checkpoint:
        checkpoint_index = int(latest_checkpoint.split(sep="ckpt-")[-1])
        status = checkpoint.restore(latest_checkpoint)
        status.expect_partial()
        tf.print(f"---Restored from {c_manager.latest_checkpoint}---")
    else:
        raise FileNotFoundError("Cannot find checkpoint")

    return checkpoint_index
