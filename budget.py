import os
import logging
import sys
import ssl

from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy

logging.basicConfig(stream=sys.stderr)

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
basedir = os.path.abspath(os.path.dirname(__file__))
context.load_cert_chain(basedir + '/server.crt', basedir + '/server.key')

from api.users import *
from api.accounts import *

if __name__ == '__main__':
    if not os.path.exists(os.path.abspath(os.path.dirname(__file__)) + '/db.sqlite'):
        db.create_all()
    app.run(ssl_context=context)
