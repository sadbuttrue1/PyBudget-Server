import os

__author__ = 'true'

SECRET_KEY = 'you-will-never-guess'
# basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
