import os

class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = "~C0MZ>4a68.+UR5!^c5H2pCs@sNBHN?_b~f]*Mgkg:3zc"
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    # PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql://cookeryuser:P@ssw0rd!@localhost:3306/cookerydb?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_SECRET_KEY = "Qfvf{Dn(sAeDE2[8;01W2Wx}}Ji<@-"
    SQLALCHEMY_ECHO = True
