import io
import os

import numpy as np
import requests

from app.utils import read_config
from flask import Flask, request

from .querier import Querier


def create_app():
    config = read_config()
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping()

    app.config.from_pyfile("config.py", silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    querier = Querier()

    @app.route("/predictions")
    def predictions():
        song = request.files["query"]
        embed = querier.predict(song)
        bytestream = io.BytesIO()
        np.save(bytestream, embed)
        requests.post(
            config["QUERY"]["INDEXER_URL"],
            files={"query": bytestream.getvalue()},
            data={"abc": "xyz"},
        )

    return app
