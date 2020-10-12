import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask
    DEVELOPMENT = False
    DEBUG = False
    TESTING = False

    # mongoengine
    MONGODB_DB = os.getenv('MONGODB_DB')
    MONGODB_HOST = os.getenv('MONGODB_HOST', '127.0.0.1')
    MONGODB_PORT = int(os.getenv('MONGODB_PORT', 27017))
    MONGODB_USERNAME = os.getenv('MONGODB_USERNAME', None)
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', None)

    # Mr Developer
    ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    LOG_DIRECTORY = '%s/log' % ROOT_DIRECTORY


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True
