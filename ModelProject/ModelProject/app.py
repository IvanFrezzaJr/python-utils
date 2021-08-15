
import os
from flask import Flask
from ModelProject.ext import database
from ModelProject.ext import config

from ModelProject.ext import cli


def create_app():
    app = Flask(__name__)

    config.init_app(app)
    database.init_app(app)
    cli.init_app(app)
    return app

