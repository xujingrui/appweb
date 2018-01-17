#encoding: utf-8

from flask_migrate import Migrate,MigrateCommand
from appweb import app
from flask_script import Manager
from exts import db
from models import UserModel,UserLoginLogModel,CmdbModel



manager = Manager(app)

migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)

if __name__ == "__main__":
    manager.run()

