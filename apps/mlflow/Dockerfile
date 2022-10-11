FROM python:3.8-bullseye

ENV MINIO_ACCESS_KEY=minio
ENV MINIO_SECRET_KEY=minio
ENV MLFLOW_S3_ENDPOINT_URL=''
ENV MINIO_BUCKET_NAME=mlflow
ENV BACKEND_STORE_URL=''
ENV MLFLOW_S3_IGNORE_TLS=true

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app/
RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT [ "./docker-entrypoint.sh" ]