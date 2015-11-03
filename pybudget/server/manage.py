from flask.ext.migrate import MigrateCommand, Migrate
from flask.ext.script import Manager

from pybudget.server.budget import app, db

__author__ = 'true'

app.config.from_object('config')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
