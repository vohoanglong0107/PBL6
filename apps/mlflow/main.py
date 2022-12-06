import argparse
from loguru import logger
import os
import subprocess
from urllib.parse import urlparse

minio_access_key = os.environ.get("MINIO_ACCESS_KEY", "minio")
minio_secret_key = os.environ.get("MINIO_SECRET_KEY", "minio123")
minio_host = os.environ.get("MINIO_HOST", "minio")
minio_port = os.environ.get("MINIO_PORT", "9000")
minio_bucket_name = os.environ.get("MINIO_BUCKET_NAME", "mlflow")
minio_uri = f"s3://{minio_bucket_name}"
default_artifact_root = f"{minio_uri}/mlruns"
artifacts_destination = f"{minio_uri}/mlartifacts"
endpoint_url = f"http://{minio_host}:{minio_port}"
os.environ["MLFLOW_S3_ENDPOINT_URL"] = endpoint_url

db_host = os.environ.get("DB_HOST", "mariadb")
db_port = os.environ.get("DB_PORT", "3306")
db_user = os.environ.get("DB_USER", "root")
db_password = os.environ.get("DB_PASSWORD", "")
db_name = os.environ.get("DB_NAME", "mlflow")
db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def create_bucket():
    import minio

    logger.info(f"Creating bucket {minio_bucket_name} at {endpoint_url}")
    try:
        endpoint = urlparse(endpoint_url).netloc
        client = minio.Minio(
            endpoint,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=False,
        )
        if not client.bucket_exists(minio_bucket_name):
            client.make_bucket(minio_bucket_name)
            logger.info("Bucket {} created".format(minio_bucket_name))
        else:
            logger.info("Bucket {} already exists".format(minio_bucket_name))
    except Exception as e:
        logger.error("Error creating bucket: {}".format(e))


def create_database():
    from sqlalchemy import create_engine
    from sqlalchemy.engine import Engine
    from sqlalchemy_utils import database_exists, create_database

    # db_url for mysql
    engine = create_engine(db_url)

    if not isinstance(engine, Engine):
        logger.error("Invalid database url")
    elif not database_exists(engine.url):
        create_database(engine.url)
        logger.info("Database {} created".format(engine.url))
    else:
        logger.info("Database {} already exists".format(engine.url))


def start_server(args):
    cmd = [
        "mlflow",
        "server",
        "--backend-store-uri",
        db_url,
        # https://github.com/mlflow/mlflow/issues/6181#issuecomment-1177231056
        # basically, when this is enable, mlflow client will skip the proxied
        # by mlflow server
        # "--default-artifact-root",
        # default_artifact_root,
        "--artifacts-destination",
        artifacts_destination,
        "--serve-artifacts",
    ]
    if args.host:
        cmd.extend(["--host", args.host])
    if args.port:
        cmd.extend(["--port", args.port])
    if args.workers:
        cmd.extend(["--workers", args.workers])
    if args.gunicorn_opts:
        cmd.extend(["--gunicorn-opts", args.gunicorn_opts])
    # run mlflow server and capture output
    logger.info("Starting mlflow server")

    subprocess_env = os.environ.copy()
    subprocess_env["AWS_ACCESS_KEY_ID"] = minio_access_key
    subprocess_env["AWS_SECRET_ACCESS_KEY"] = minio_secret_key
    server = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        env=subprocess_env,
    )
    for line in iter(server.stdout.readline, ""):
        print(line, end="")


def main(args):
    create_bucket()
    create_database()
    start_server(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", default="5000")
    parser.add_argument("--workers", default="1")
    parser.add_argument("--static-prefix", default="/")
    parser.add_argument("--gunicorn-opts", default=None)

    args = parser.parse_args()
    main(args)
