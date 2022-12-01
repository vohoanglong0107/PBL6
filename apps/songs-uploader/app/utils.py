from io import BytesIO

from google.cloud import storage
from pydub import AudioSegment
from werkzeug.datastructures import FileStorage


def convert_to_wav_8000hz_format(song: FileStorage):
    song = AudioSegment.from_file(song)
    song = song.set_frame_rate(8000)
    bytestream = BytesIO()
    bytestream.name = song.filename
    song.export(bytestream, format="wav")

    return bytestream


def upload_to_gcs(bucketname, file):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file()
