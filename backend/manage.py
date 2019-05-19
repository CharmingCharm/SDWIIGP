from app import create_app
from flask_script import Manager, Server
from flask_migrate import MigrateCommand
from app.extension import db, rq
from app.model import User, Problem
import os

config_name = os.environ.get('FLASK_CONFIG') or 'default'

app = create_app(config_name)

manager = Manager(app)

manager.add_command('db', MigrateCommand)
# manager.add_command('runserver', Server(use_debugger = True))

@manager.command
def judger():
    worker = rq.get_worker()
    worker.work()

@manager.command
def adduser(name, pwd, teacher):
    is_teacher = teacher == 'true'
    db.session.add(User(user_name = name, password = pwd, is_teacher = is_teacher))
    db.session.commit()

if __name__ == '__main__':
    manager.run()
