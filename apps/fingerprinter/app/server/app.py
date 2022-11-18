import os
import requests
from flask import Flask, request
import io
import numpy as np
from .querier import Querier
from app.utils import read_config

def create_app():
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
        requests.post(, files={"query": bytestream.getvalue()}, data={"abc": "xyz"})

    return app
