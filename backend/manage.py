from app import create_app
from flask_script import Manager, Server
from flask_migrate import MigrateCommand
import os

config_name = os.environ.get('FLASK_CONFIG') or 'default'

# 生成app
app = create_app(config_name)

manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(use_debugger = True))

if __name__ == '__main__':
    manager.run()
