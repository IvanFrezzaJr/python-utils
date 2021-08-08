import argparse as ap
import os
import shutil


def main(args):

    name = args.name
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)

    if os.path.isdir(path):
        resp = input("project exists. would you like to overwrite? (s/n): ")
        if str.upper(resp) != "s":
            return None
        shutil.rmtree(path)

    create_boilerplate(path)


def create_boilerplate(path_project):

    name = os.path.basename(path_project)
    path = os.path.dirname(path_project)

    # root folder
    os.mkdir(path_project)
    os.mkdir(os.path.join(path_project, "tests"))
    # os.mkdir(os.path.join(path,"migrations"))

    # root files
    _create_file(os.path.join(path_project, ".env"), _write_env_file(name))
    _create_file(os.path.join(path_project, "makefile"), _write_makefile(name))
    _create_file(os.path.join(path_project, "setup.py"), _write_setup_file(name))
    _create_file(os.path.join(path_project, "requirements.txt"), _write_requirements())
    _create_file(
        os.path.join(path_project, "requirements-dev.txt"), _write_requirements_dev()
    )
    _create_file(os.path.join(path_project, "license"))
    _create_file(os.path.join(path_project, "readme.rst"))

    # project folder
    project_path = os.path.join(path_project, name)
    os.mkdir(project_path)
    # project files
    _create_file(os.path.join(project_path, "__init__.py"))
    _create_file(os.path.join(project_path, "app.py"), _write_app_file(name))

    # ext and blueprint folder
    ext_path = os.path.join(project_path, "ext")
    os.mkdir(ext_path)
    # blueprint_path = os.path.join(project_path, "blueprints")
    # os.mkdir(blueprint_path)

    # ext folder
    _create_file(os.path.join(ext_path, "__init__.py"))
    # _create_file(os.path.join(ext_path, "cors.py"), _write_cors_file())
    _create_file(os.path.join(ext_path, "config.py"), _write_config_file(name))
    _create_file(os.path.join(ext_path, "migration.py"), _write_migration_file(name))
    _create_file(os.path.join(ext_path, "cli.py"), _write_cli_file(name))

    # _create_file(os.path.join(ext_path, "debug.py"))
    # _create_file(os.path.join(ext_path, "errorhandler.py"))
    # _create_file(os.path.join(ext_path, "jwt.py"))
    # _create_file(os.path.join(ext_path, "mail.py"))
    # _create_file(os.path.join(ext_path, "auth.py"))

    # database folder
    database_path = os.path.join(ext_path, "database")
    os.mkdir(database_path)
    # database files
    _create_file(os.path.join(database_path, "__init__.py"), _write_ext_database_file())
    _create_file(
        os.path.join(database_path, "command.py"), _write_ext_database_command_file(name)
    )
    # database models folder
    models_path = os.path.join(database_path, "models")
    os.mkdir(models_path)
    _create_file(os.path.join(models_path, "base.py"))
    _create_file(os.path.join(models_path, "user.py"), __write_model_user_file(name))
    """
    
    # blueprint folder
    _create_file(os.path.join(blueprint_path, "__init__.py"))
    webui_path = os.path.join(blueprint_path, "webui")
    os.mkdir(webui_path)
    resapi_path = os.path.join(blueprint_path, "resapi")
    os.mkdir(resapi_path)

    # resapi folder
    _create_file(os.path.join(resapi_path, "__init__.py"))
    _create_file(os.path.join(resapi_path, "routes.py"))
    os.mkdir(os.path.join(resapi_path, "resources"))

    # webui folder
    _create_file(os.path.join(webui_path, "__init__.py"))
    _create_file(os.path.join(webui_path, "views.py"))
    template_path = os.path.join(webui_path, "templates")
    os.mkdir(template_path)
    _create_file(os.path.join(template_path, "index.html"))
    """
    print("project created successfully")


def _create_file(path, content=""):
    with open(path, "x") as f:
        f.write(content)
    return True


def _write_setup_file(project_name):
    return (
        """
from setuptools import setup, find_packages


def read(filename):
    return [
        reg.strip() 
        for reg 
        in open(filename).readlines()
    ]


extras = {
    'develop': read('requirements-dev.txt')
}


setup(
    name='"""
        + project_name
        + """',
    version="0.1.0",
    description='"""
        + project_name
        + """ project',
    packages=find_packages(exclude=".venv"),
    include_package_data=True,
    install_requires=read("requirements.txt"),
    extras_require={
        'dev': read("requirements-dev.txt")
    },
)
    """
    )


def _write_requirements():
    return """
flask
Flask-SQLAlchemy
flask-cors
"""


def _write_requirements_dev():
    return """
black
flake8
flask-shell-ipython
ipdb
ipython
isort
pytest
pytest-flask
pytest-cov
python-dotenv
"""


def _write_makefile(name):
    return (
        """
clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
	pip install -e .[dev] --upgrade --no-cache

install:
	pip install -e .[dev]

test:
	pytest tests/ -v --cov="""
        + name
        + """

env:
	python -m venv .venv ;\
	.venv\scripts\activate


"""
    )


def _write_app_file(name):
    return (
        """
import os
from flask import Flask
from """
        + name
        + """.ext import database
from """
        + name
        + """.ext import config

from """
        + name
        + """.ext import cli


def create_app():
    app = Flask(__name__)

    config.init_app(app)
    database.init_app(app)
    cli.init_app(app)
    return app

"""
    )


def _write_config_file(name):
    return (
        '''


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
    application_root = "/'''
        + name
        + """"



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



"""
    )


def _write_ext_database_command_file(name):
    return (
        """
from """
        + name
        + """.ext.database import db
from """
        + name
        + '''.ext.database.models.user import User


def create_db():
    """Creates database"""
    db.create_all()


def drop_db():
    """Cleans database"""
    db.drop_all()


def populate_db():
    """Populate db with sample data"""
    data = [
        User(username="Joao Silva", email="joao.silva@gmail.com"),
        User(username="Ana Maria", email="ana.maria@gmail.com"),
    ]
    db.session.bulk_save_objects(data)
    db.session.commit()
    return User.query.all()

    '''
    )


def __write_database_base_file(name):
    return (
        """
from """+ name +""".ext.database import db
from flask import abort
from datetime import datetime

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(
        db.DateTime(),
        nullable=False,
        default=datetime.now,
        server_default=db.func.now())
    updated_at = db.Column(db.DateTime(),
        nullable=False,
        default=datetime.now,
        server_default=db.func.now(),
        server_onupdate=db.func.now())


    @classmethod
    def create(model, data):
        item = model(**data)
        try:
            
            db.session.add(item)
            db.session.commit()
            return item
        except Exception as e:
            db.session.rollback()


    @classmethod
    def delete_by_id(model, id):
        item = model.query.get(id) or abort(404, "item not found")
        try:
            db.session.delete(item)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()



    @classmethod
    def update_by_id(model, id, data):
        try:
            query = model.query.filter(model.id == id)
            if data:
                query.update(data)
                db.session.commit()
                item = query.first()            
                return item
        except Exception as e:
            db.session.rollback()



    @classmethod
    def get_by_id(model, id):
        data = model.query.get(id) or abort(404, "item not found")
        return data


    @classmethod
    def get_all(model):
        return model.query.all()

    @classmethod
    def get_list(model, args):
        args = dict(args)
        
        query = model.filters(args, model.query)
        data = query.all()
        return {
            "data": data,
            "meta": {}
        }, 200

    @classmethod
    def filters(model, args, query):

        filter_args = args.copy()

        if len(filter_args) < 1:
            return query

        filters = []
        for arg in args:
            attr = model.get_attr(arg)
            value = args[arg]
            filters.append(attr == value)

        return query.filter(*filters)


        """
    )

def __write_model_user_file(name):
    return (
        """
    
from """
        + name
        + """.ext.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username

    """
    )


def _write_migration_file(name):
    return (
        """
from flask_migrate import Migrate
from """
        + name
        + """.ext.database import db

migrate = Migrate()


def init_app(app):
    migrate.init_app(app, db)

    
    """
    )


def _write_cli_file(name):
    return (
        """
from """
        + name
        + """.ext.database.command import create_db, drop_db, populate_db

def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db, populate_db]:
        app.cli.add_command(app.cli.command()(command))
"""
    )


def _write_ext_database_file():
    return """
  
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)
"""


def _write_env_file(name, user="user", password="password"):
    return (
        """
flask_app="""
        + name
        + """.app:create_app
flask_env=development
prod_database_uri=postgresql://"""
        + user
        + """:"""
        + password
        + """@"""
        + name
        + """/"""
        + name
        + """
dev_database_uri=postgresql://"""
        + user
        + """:"""
        + password
        + """@localhost/"""
        + name
        + """
test_database_uri=postgresql://"""
        + user
        + """:"""
        + password
        + """@localhost/"""
        + name
        + """
staging_database_uri=postgresql://"""
        + user
        + """:"""
        + password
        + """@"""
        + name
        + """/"""
        + name
        + """
"""
    )


def _write_cors_file():
    return """
from flask_cors import CORS

cors = CORS()

def init_app(app):
    cors.init_app(app)
"""


if "__main__" == __name__:

    parser = ap.ArgumentParser(description="create flask boilerplate")
    parser.add_argument("-i", "--init", required=False, help="init boilerplate")
    parser.add_argument("-n", "--name", required=True, help="project name")

    args = parser.parse_args()

    main(args)
