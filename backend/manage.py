from app import create_app
from flask_script import Manager, Server
from flask_migrate import MigrateCommand
from app.extension import db
from app.model import User, Problem
import os

config_name = os.environ.get('FLASK_CONFIG') or 'default'

# 生成app
app = create_app(config_name)

manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(use_debugger = True))

@manager.command
def adduser(name, pwd, teacher):
    is_teacher = True if teacher == 'true' else False
    db.session.add(User(user_name = name, password = pwd, is_teacher = is_teacher))
    db.session.commit()

if __name__ == '__main__':
    manager.run()
