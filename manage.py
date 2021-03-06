from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from db import db

app = Flask(__name__)
app.config.from_object('settings.DevelopmentConfig')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from models.user import *
from models.dish import *

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    manager.run()
