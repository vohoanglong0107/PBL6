FROM python:3.8-bullseye as builder


WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
# BUILDKIT cache
RUN --mount=type=cache,target=/root/.cache/pip \
  pip install --no-cache-dir -r requirements.txt

FROM python:3.8-slim

COPY --from=builder /opt/venv /opt/venv

ENV MINIO_ACCESS_KEY=minio
ENV MINIO_SECRET_KEY=minio
ENV MINIO_HOST=minio
ENV MINIO_PORT=9000
ENV MINIO_BUCKET_NAME=mlflow
ENV MLFLOW_S3_IGNORE_TLS=true
ENV DB_HOST=mariadb
ENV DB_PORT=3306
ENV DB_USERNAME=host
ENV DB_PASSWORD=''
ENV DB_NAME=mariadb

WORKDIR /app
COPY . /app/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PATH="/opt/venv/bin:$PATH"

CMD [ "python", "main.py" ]