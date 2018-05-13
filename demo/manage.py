# encoding=utf-8
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app.models import App,Admin,Theta,Platform,KeyWord,Comment,User
from demo import app
from exts import db

migrate =Migrate(app,db)
manager = Manager(app)

@manager.command
def runserver():
	print("服务器跑起来了")

# db.create_all()
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
	manager.run()