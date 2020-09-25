import os

from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))


class BaseConfig:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/workos.db"

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tmp/workos_test.db'

class ProductionConfig(BaseConfig):
    DEBUG = False
    DATABASE = "mysql"
    DATABASE_DRIVER = "pymysql"
    DB_USERNAME = os.getenv('RDS_USER')
    DB_PASSWORD = os.getenv('RDS_PASSWORD')
    DATBASE_HOST = os.getenv('RDS_HOST')
    DATABASE_PORT = os.getenv('RDS_PORT')
    DATABASE_NAME = os.getenv('RDS_DATABASE')

    SQLALCHEMY_DATABASE_URI = (
        f"{DATABASE}+{DATABASE_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}"
        f"@{DATBASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )

config_mapper = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
