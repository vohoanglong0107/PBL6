import io

import numpy as np

from flask import request

from .app import app, db, index
from .indexer import search


@app.route("/", methods=["GET", "POST"])
def res():
    request_files = request.files
    query = request_files["query"]
    query = np.load(io.BytesIO(query.read()))
    candidates = search(index, query, db)
    return {"candidates": candidates.tolist()}


@app.route("/healthz", methods=["GET"])
def healtz():
    return "oke"
