#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

BACKEND_STORE_URL=${BACKEND_STORE_URL:-}
MINIO_BUCKET_NAME=${MINIO_BUCKET_NAME:-mlflow}

echo "BACKEND_STORE_URL: $BACKEND_STORE_URL"
echo "MINIO_BUCKET_NAME: $MINIO_BUCKET_NAME"

python ./init_minio_bucket.py

mlflow server \
  --backend-store-uri ${BACKEND_STORE_URL} \
  --default-artifact-root s3://${MINIO_BUCKET_NAME} \
  --host 0.0.0.0 \
  --port 5000