import logging

from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from settings import *
from routes import register_routes

from db import db
from extensions import *

def create_app(env):
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
