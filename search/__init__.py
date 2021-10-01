import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
import logging
from logging.config import fileConfig
from . import settings

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config.from_object(settings)
csrf = CSRFProtect()
csrf.init_app(app)
app.config["SECRET_KEY"] = SECRET_KEY
fileConfig("logging/logging.ini")
logging.basicConfig()
logger = logging.getLogger(__name__)

from . import routes  # noqa: F401 isort:skip
