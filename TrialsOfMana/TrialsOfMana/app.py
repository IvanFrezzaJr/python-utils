import os
from flask import Flask
from TrialsOfMana.ext import config
from TrialsOfMana.ext import database
from TrialsOfMana.ext import migration
from TrialsOfMana.ext.database import cli


def create_app():
    app = Flask(__name__)
    config.init_app(app)
    database.init_app(app)
    migration.init_app(app)
    cli.init_app(app)
    return app
