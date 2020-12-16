import logging

from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from routes import register_routes

from db import db
from extensions import *
from datetime import datetime as dt

def setup_test():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = "~C0MZ>4a68.+UR5!^c5H2pCs@sNBHN?_b~f]*Mgkg:3zc"
    app.config['JWT_SECRET_KEY'] = "Qfvf{Dn(sAeDE2[8;01W2Wx}}Ji<@-"
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://cookerytestuser:Abc123!xyz###@localhost:3306/cookery_test_db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False

    db.init_app(app)

    return app

def create_app(env):
    import settings

    app = Flask(__name__)

    if env == "production":
        app.config.from_object('settings.ProductionConfig')
    elif env == "staging":
        app.config.from_object('settings.StagingConfig')
    else:
        app.config.from_object('settings.DevelopmentConfig')

    api = Api(app)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    register_extensions(app)
    register_routes(api)

    # logger = logging.getLogger("app.access")
    # logging.info('info on app.vue')

    return app

def register_extensions(app):
    logs.init_app(app)
    db.init_app(app)

    return None

def main():
    create_app("dev")
    app.run()

if __name__ == '__main__':
    # from db import db
    # db.init_app(app)
    # initialize_routes(api)
    # app.run(port=5000, debug=True)
    main()
