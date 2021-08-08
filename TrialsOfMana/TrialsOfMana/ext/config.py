


"""Flask configuration."""
import os
import logging


def init_app(app):

    settings = {
        "production": ProdConfig,
        "development": DevConfig,
        "test": TestConfig,
        "local": LocalConfig,
        "staging": StagingConfig,
    }

    ENV = os.environ.get("FLASK_ENV")

    if env_class := settings.get(ENV):
            app.config.from_object(env_class)
    else: 
        environments = ", ".join(settings.keys())
        message = f"[ERROR] FLASK_ENV='{ENV}' is not valid. Try to set one of those: {environments}"
        raise KeyError(message)


class Config:
    """Base config."""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_NAME = os.environ.get("SESSION_COOKIE_NAME")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    APPLICATION_ROOT= "/TrialsOfMana"


class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("PROD_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_URI = os.environ.get("PROD_DATABASE_URI")
    FTP_HOST= os.environ.get("PROD_FTP_HOST", "20.0.0.10")


class DevConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DB_URI = os.environ.get("DEV_DATABASE_URI")
    FTP_HOST= os.environ.get("DEV_FTP_HOST", "20.0.0.11")


class TestConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DB_URI = os.environ.get("TEST_DATABASE_URI")
    FTP_HOST=  os.environ.get("TEST_FTP_HOST", "20.0.0.11")


class LocalConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("LOCAL_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DB_URI = os.environ.get("LOCAL_DATABASE_URI", "localhost")
    FTP_HOST=  os.environ.get("LOCAL_FTP_HOST", "20.0.0.11")


class StagingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("STAGING_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DB_URI = os.environ.get("STAGING_DATABASE_URI")
    FTP_HOST= os.environ.get("LOCAL_FTP_HOST", "20.0.0.19")

