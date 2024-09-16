import logging
from flask import Flask
from flask_appbuilder import SQLA, AppBuilder

from api.auth.extentions.init_auth_manager import init_auth_manager

"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_pyfile("settings.py")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)


init_auth_manager(appbuilder)

from . import views