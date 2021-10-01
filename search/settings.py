import os
from . import readenv

SQLALCHEMY_DATABASE_URI = (
    "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}".format(
        **os.environ
    )
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_METHODS = "{WTF_CSRF_METHODS}".format(**os.environ)
