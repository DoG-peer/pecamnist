import os
basedir = os.path.abspath(os.path.dirname(__file__))

if 'DATABASE_URL' in os.environ:
	DATABASE_URL = os.environ["DATABASE_URL"]
else:
	import secret
	DATABASE_URL = secret.DATABASE_URL
class Config():
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = ''
	SQLALCHEMY_DATABASE_URI = DATABASE_URL
	LEARNED = False
class ProductionConfig(Config):
	DEBUG = False

class LearnedProductionConfig(ProductionConfig):
	LEARNED = True

class StagingConfig(Config):
	DEVELOPMENT = True
	DEBUG = True
class LearnedStagingConfig(StagingConfig):
	LEARNED = True

class TestingConfig(Config):
	TESTING = True



