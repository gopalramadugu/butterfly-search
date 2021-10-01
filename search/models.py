import datetime as dt

from flask_sqlalchemy import SQLAlchemy

from . import app

db = SQLAlchemy(app)


class Search(db.Model):
    __tablename__ = "searchpreferences"

    id = db.Column(db.Integer, primary_key=True)
    appuserid = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, nullable=True)
    searchtype = db.Column(db.Text, nullable=False)
    searchcriteria = db.Column(db.JSON, nullable=False)
    isdeleted = db.Column(db.Boolean, nullable=False)
    createddate = db.Column(db.DateTime, default=dt.datetime.utcnow, nullable=False)
    createdby = db.Column(db.Integer, nullable=False)
    updateddate = db.Column(db.DateTime, default=dt.datetime.utcnow, nullable=False)
    updatedby = db.Column(db.Integer, nullable=False)
