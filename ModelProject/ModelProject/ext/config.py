


"""flask configuration."""
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


    env = os.environ.get("flask_env")

    if env_class := settings.get(env):
            app.config.from_object(env_class)
    else: 
        environments = ", ".join(settings.keys())
        message = f"[error] flask_env='{env}' is not valid. try to set one of those: {environments}"
        raise KeyError(message)


class Config:
    """base config."""

    secret_key = os.environ.get("secret_key")
    session_cookie_name = os.environ.get("session_cookie_name")
    static_folder = "static"
    templates_folder = "templates"
    application_root = "/ModelProject"



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



