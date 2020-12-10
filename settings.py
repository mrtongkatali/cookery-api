import os
from environs import Env

env = Env()

class DevelopmentConfig():
    env.read_env(".env.dev", recurse=False)

    SECRET_KEY = env.str('SECRET_KEY')
    DEBUG = env.bool('DEBUG')
    # PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI=env.str('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')
    SQLALCHEMY_ECHO = True

class StagingConfig():
    env.read_env(".env.dev", recurse=False)

    SECRET_KEY = env.str('SECRET_KEY')
    DEBUG = env.bool('DEBUG')
    # PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI=env.str('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')
    SQLALCHEMY_ECHO = True

class ProductionConfig():
    env.read_env(".env.dev", recurse=False)

    SECRET_KEY = env.str('SECRET_KEY')
    DEBUG = env.bool('DEBUG')
    # PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI=env.str('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')
    SQLALCHEMY_ECHO = True

class TestConfig():
    env.read_env(".env.dev", recurse=False)

    SECRET_KEY = env.str('SECRET_KEY')
    DEBUG = env.bool('DEBUG')
    # PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI=env.str('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')
    SQLALCHEMY_ECHO = True
