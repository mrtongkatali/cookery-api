import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://cookeryuser:P@ssw0rd!@localhost:3306/cookerydb?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_ECHO = True
