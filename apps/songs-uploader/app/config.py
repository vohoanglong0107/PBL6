from os import environ, path

from dotenv import load_dotenv


basedir = path.abspath(path.dirname(path.dirname(__file__)))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Set Flask config variables."""

    SECRET_KEY = environ.get("SECRET_KEY", "secret-key")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": int(environ.get("SQLALCHEMY_POOL_SIZE", "10")),
        "pool_recycle": int(environ.get("SQLALCHEMY_POOL_RECYCLE", "3600")),
        "pool_pre_ping": environ.get("SQLALCHEMY_POOL_RECYCLE")
        if environ.get("SQLALCHEMY_POOL_RECYCLE")
        else True,
    }

    GCS_BUCKET = environ.get("GCS_BUCKET")
    GCS_SONG_DIRECTORY = environ.get("GCS_SONG_DIRECTORY")

    FINGERPRINTER_URL = environ.get("FINGERPRINTER_URL")

    CACHE_TYPE = environ.get("CACHE_TYPE")
    CACHE_REDIS_HOST = environ.get("CACHE_REDIS_HOST")
    CACHE_REDIS_PORT = environ.get("CACHE_REDIS_PORT")
    CACHE_DEFAULT_TIMEOUT = environ.get("CACHE_DEFAULT_TIMEOUT")


class ProductionConfigkConfigk:
    pass


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
