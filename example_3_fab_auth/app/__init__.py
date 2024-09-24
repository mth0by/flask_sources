import logging
import os

from flask import Flask
from flask_appbuilder import SQLA, AppBuilder

from app.extentions import init_appbuilder_views

from pathlib import Path

CONF_FILENAME = "settings.py"
CONF_FILEPATH = Path(os.getcwd(), CONF_FILENAME)

# Logging configuration
logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_pyfile(CONF_FILEPATH)

db = SQLA(app)
db.init_app(app)

with app.app_context():
    appbuilder = AppBuilder(app, db.session)

    init_appbuilder_views(app)
