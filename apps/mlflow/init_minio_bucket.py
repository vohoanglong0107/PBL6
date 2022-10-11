import argparse
from loguru import logger
import minio
import os
from urllib.parse import urlparse

def create_bucket():
  access_key = os.environ.get('MINIO_ACCESS_KEY')
  secret_key = os.environ.get('MINIO_SECRET_KEY')
  endpoint_URL = os.environ.get('MLFLOW_S3_ENDPOINT_URL')
  bucket_name = os.environ.get('MINIO_BUCKET_NAME')
  logger.info(f"Creating bucket {bucket_name} at {endpoint_URL}")
  try:
    endpoint = urlparse(endpoint_URL).netloc
    client = minio.Minio(
      endpoint,
      access_key=access_key,
      secret_key=secret_key,
      secure=False
    )
    if not client.bucket_exists(bucket_name):
      client.make_bucket(bucket_name)
      logger.info('Bucket {} created'.format(bucket_name))
    else:
      logger.info('Bucket {} already exists'.format(bucket_name))
  except Exception as e:
    logger.warning('Error creating bucket: {}'.format(e))

def main(args):
  create_bucket()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--ret')
  args = parser.parse_args()
  main(args)

