import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from harvestapi.model import db
from run_api import create_app

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
