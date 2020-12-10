import logging
from logging import Formatter, FileHandler

from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from settings import *
from routes import initialize_routes

from db import db

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

    initialize_routes(api)
    db.init_app(app)

    return app

def main():
    create_app("dev")
    app.run()

if __name__ == '__main__':
    # from db import db
    # db.init_app(app)
    # initialize_routes(api)
    # app.run(port=5000, debug=True)
    main()
