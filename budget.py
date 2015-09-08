import os
import logging
import sys

from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy

logging.basicConfig(stream=sys.stderr)

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

from api import *

if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run()
