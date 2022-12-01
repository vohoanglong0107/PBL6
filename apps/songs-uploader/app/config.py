from os import environ, path

from dotenv import load_dotenv


basedir = path.abspath(path.dirname(path.dirname(__file__)))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Set Flask config variables."""

    SECRET_KEY = environ.get("SECRET_KEY")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
