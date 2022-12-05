import io
import os
import tempfile
import traceback
import uuid

import numpy as np
import requests

from app.utils import read_config
from flask import Flask, make_response, request
from loguru import logger

from .querier import Querier


def create_app():
    config = read_config()
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    querier = Querier()

    @app.route("/predictions", methods=["GET"])
    def predictions():
        song = request.files["query"]
        temp_file_name = str(uuid.uuid4())
        temp_file_path = os.path.join(tempfile.gettempdir(), temp_file_name)
        song.save(temp_file_path)
        logger.info(f"received file{song}")
        try:
            embed = querier.predict(temp_file_path)
            bytestream = io.BytesIO()
            bytestream.name = song.filename
            np.save(bytestream, embed)

            logger.info(f"predicted embedding{embed}")
            r = requests.post(
                config["QUERY"]["INDEXER_URL"],
                files={"query": bytestream.getvalue()},
            )
            r.raise_for_status()
            candidates = r.json()["candidates"]
            logger.info(f"received candidates {candidates}")

            # r = requests.get(config["SONGS_UPLOADER"]["URL"], params=candidates)
            # r.raise_for_status()
            # response = make_response(r.json()["data"])
            response = candidates
            return response
        except Exception as e:
            traceback.print_exc()
            response = make_response(str(e), 500)
            return response
        finally:
            os.remove(temp_file_path)

    @app.route("/healthz", methods=["GET"])
    def healthz():
        return "oke"

    return app
