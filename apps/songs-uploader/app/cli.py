#!/usr/bin/env python3

import os

import click

from .app import app
from .db import db
from .models import Song
from .utils import download_from_gcs, get_gcs_bucket


@click.command()
@click.argument("output_directory")
def download_song(output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    with app.app_context():
        songs = db.session.execute(db.select(Song)).scalars()

        gcs_bucket_name = app.config["GCS_BUCKET"]
        gcs_bucket = get_gcs_bucket(gcs_bucket_name)
        for song in songs:
            open(os.path.join(output_directory, f"{song.id}.wav"), "a").close()
            download_from_gcs(
                gcs_bucket, song.url, os.path.join(output_directory, f"{song.id}.wav")
            )


if __name__ == "__main__":
    download_song()
