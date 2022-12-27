import requests

from flask import flash, jsonify, redirect, render_template, request
from loguru import logger

from .app import app, cache
from .db import db
from .models import Song
from .utils import convert_to_wav_8000hz_format, get_gcs_bucket, upload_to_gcs


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if "song" not in request.files:
        flash("You haven't uploaded anyfile")
        return redirect(request.url)

    song = request.files["song"]
    if not song.filename:
        flash("Song don't have filename")
        return redirect(request.url)

    converted_song = convert_to_wav_8000hz_format(song)
    gcs_bucket_name = app.config["GCS_BUCKET"]
    gcs_song_directory = app.config["GCS_SONG_DIRECTORY"]
    gcs_bucket = get_gcs_bucket(gcs_bucket_name)
    url = upload_to_gcs(gcs_bucket, gcs_song_directory, converted_song)

    db.session.add(
        Song(title=request.form["title"], artist=request.form["artist"], url=url)
    )
    db.session.commit()

    return redirect("/songs")


@app.route("/songs", methods=["GET"])
@cache.cached(timeout=50)
def songs():
    songs = db.session.execute(db.select(Song)).scalars().all()
    return render_template("songs.html", songs=songs)


@app.route("/api/songs", methods=["GET"])
@cache.cached(timeout=50)
def songs_api():
    songs = db.session.execute(db.select(Song)).scalars().all()
    return jsonify([song.as_dict() for song in songs])


@app.route("/api/predictions", methods=["GET", "POST"])
def predictions():
    query = request.files["query"]
    query = convert_to_wav_8000hz_format(query)
    r = requests.get(
        app.config["FINGERPRINTER_URL"],
        files={"query": query},
    )
    r.raise_for_status()

    logger.info(r.json())
    candidates_index = r.json()
    candidates_info = (
        db.session.execute(db.select(Song).where(Song.id.in_(candidates_index)))
        .scalars()
        .all()
    )
    return jsonify([candidate_info.as_dict() for candidate_info in candidates_info])


@app.route("/healthz", methods=["GET"])
def healthz():
    return "oke"
