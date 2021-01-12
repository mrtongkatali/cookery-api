import os
from environs import Env

env = Env()

class Config():
    LOG_TYPE = env.str("LOG_TYPE", "debug")  # Default is a Stream handler
    LOG_LEVEL = env.str("LOG_LEVEL", "DEBUG")

    # File Logging Setup
    LOG_DIR = env.str("LOG_DIR", "/var/log/crazyapp/cookery")
    APP_LOG_NAME = env.str("APP_LOG_NAME", "app.log")
    WWW_LOG_NAME = env.str("WWW_LOG_NAME", "www.log")
    LOG_MAX_BYTES = env.int("LOG_MAX_BYTES", 100_000_000)  # 100MB in bytes
    LOG_COPIES = env.int("LOG_COPIES", 5)

class DevelopmentConfig(Config):
    env.read_env(".env.dev", recurse=False)

    SECRET_KEY = env.str('SECRET_KEY')
    DEBUG = env.bool('DEBUG')
    # PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI=env.str('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')
    SQLALCHEMY_ECHO = False
    ELASTICSEARCH_URL = env.str('ELASTICSEARCH_URL')

class StagingConfig(Config):
    env.read_env(".env.dev", recurse=False)

    SECRET_KEY = env.str('SECRET_KEY')
    DEBUG = env.bool('DEBUG')
    # PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI=env.str('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')
    SQLALCHEMY_ECHO = False
    ELASTICSEARCH_URL = env.str('ELASTICSEARCH_URL')

class ProductionConfig(Config):
    env.read_env(".env.dev", recurse=False)

    SECRET_KEY = env.str('SECRET_KEY')
    DEBUG = env.bool('DEBUG')
    # PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI=env.str('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')
    SQLALCHEMY_ECHO = False
    ELASTICSEARCH_URL = env.str('ELASTICSEARCH_URL')

class TestConfig(Config):
    env.read_env(".env.testing", recurse=False)

    SECRET_KEY = env.str('SECRET_KEY')
    DEBUG = env.bool('DEBUG')
    # PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI=env.str('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')
    SQLALCHEMY_ECHO = False
    ELASTICSEARCH_URL = env.str('ELASTICSEARCH_URL')
