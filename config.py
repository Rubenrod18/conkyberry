import os


class Config():
    # Flask
    DEVELOPMENT = False
    DEBUG = False
    TESTING = False

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
