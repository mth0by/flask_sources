import logging
import os

from flask import Flask
from flask_login import LoginManager

from pathlib import Path

CONF_FILENAME = "config.py"
CONF_FILEPATH = Path(os.getcwd(), CONF_FILENAME)

# Logging configuration
logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_pyfile(CONF_FILEPATH)

with app.app_context():
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.auth.views import auth
    from app.common.views import common

    app.register_blueprint(auth)
    app.register_blueprint(common)

    from app.database import init_db

    init_db()