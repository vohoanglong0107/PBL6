import os


class Config:
    """Set Flask config variables."""

    INDEX_PATH = os.environ.get("INDEX_PATH", "")
    EMB_DIR = os.environ.get("EMB_DIR", "")
    ARTIFACT_ENPOINT_URL = os.environ.get("ARTIFACT_ENPOINT_URL", "")
    ARTIFACT_BUCKET = os.environ.get("ARTIFACT_BUCKET", "")
    INDEX_ARTIFACT_KEY = os.environ.get("INDEX_ARTIFACT_KEY", "")
    EMB_ARTIFACT_KEY = os.environ.get("EMB_ARTIFACT_KEY", "")
