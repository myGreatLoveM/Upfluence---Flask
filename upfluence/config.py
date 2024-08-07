import secrets
import os
import random

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = secrets.token_urlsafe()
    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "password"

    UPLOADS = "/assets/images/prod/uploads"

    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "password"

    UPLOADS = "/assets/images/dev/uploads"


class TestConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "password"

    UPLOADS = "/assets/images/test/uploads"
