import os
from .common.constants import INSTANCE_FOLDER_PATH

class BaseConfig(object):

    PROJECT = "app"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    ENV = 'development'
    DEBUG = False
    TESTING = False

    ADMINS = ["iman.m93@gmail.com"]

    # TODO: Implement more secure secret key
    SECRET_KEY = "secret_key"


class DefaultConfig(BaseConfig):

    # Debug environment
    DEBUG = True

    # TODO: Make this more secure for production environments
    SECRET_KEY = "development_key"


class DevConfig(DefaultConfig):
    """ Development Configuration """

    # Celery config details
    CELERY_RESULT_BACKEND = 'rpc://'
    CELERY_BROKER_URL = 'amqp://admin:pass@rabbit:5672'

class TestConfig(DevConfig):
    """ Testing Configuration """
    TESTING = True

class StagingConfig(DefaultConfig):
    """ Staging Configuration """
    pass


class ProdConfig(DefaultConfig):
    """ Production Configuration """
    pass


def get_config(MODE):
    SWITCH = {
        'DEV'     : DevConfig,
        'TEST'    : TestConfig,
        'STAGING' : StagingConfig,
        'PROD'    : ProdConfig
    }
    return SWITCH[MODE]
