import os

from io import BytesIO

from google.cloud import storage
from pydub import AudioSegment
from werkzeug.datastructures import FileStorage


def convert_song_name(name):
    return os.path.splitext(name)[0] + ".wav"


def convert_to_wav_8000hz_format(song: FileStorage):
    filename = song.filename
    song = AudioSegment.from_file(song)
    song = song.set_frame_rate(8000)
    song = song.set_channels(1)
    bytestream = BytesIO()
    bytestream.name = convert_song_name(filename)
    song.export(bytestream, format="wav")

    return bytestream


def get_gcs_bucket(
    bucket_name: str,
):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    return bucket


def upload_to_gcs(bucket: storage.Bucket, bucket_directory: str, file: BytesIO):
    blob = bucket.blob(os.path.join(bucket_directory, file.name))
    blob.upload_from_file(file)
    return blob.name


def download_from_gcs(bucket: storage.Bucket, url: str, dest: str):
    blob = bucket.blob(url)
    blob.download_to_filename(dest)
