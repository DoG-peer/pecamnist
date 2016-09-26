import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

if 'APP_SETTINGS' in os.environ:
	app_settings = os.environ['APP_SETTINGS']
else:
	app_settings = "config.StagingConfig"
app.config.from_object(app_settings)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def clean():
	from models import Image
	Image.clean(db)
	db.session.commit()


if __name__ == '__main__':
	manager.run()



