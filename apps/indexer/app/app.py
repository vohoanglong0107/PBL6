import os

from flask import Flask

from .indexer import load_index, load_memmap_data
from .utils import download_artifact


app = Flask(__name__, instance_relative_config=True)
app.config.from_object("app.config.Config")
download_artifact(
    app.config["ARTIFACT_ENPOINT_URL"],
    app.config["ARTIFACT_BUCKET"],
    app.config["INDEX_ARTIFACT_KEY"],
    app.config["INDEX_PATH"],
    tar_zip=True,
)
download_artifact(
    app.config["ARTIFACT_ENPOINT_URL"],
    app.config["ARTIFACT_BUCKET"],
    app.config["EMB_ARTIFACT_KEY"],
    app.config["EMB_DIR"],
    tar_zip=True,
)
index = load_index(app.config["INDEX_PATH"])
db, _ = load_memmap_data(app.config["EMB_DIR"], "db")
index.add(db)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass
