import os
from flask import Flask
from NewOne.ext import config
from NewOne.ext import database
from NewOne.ext import cli


def create_app():
    app = Flask(__name__)

    config.init_app(app)
    database.init_app(app)
    cli.init_app(app)
    return app
