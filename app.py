import logging

from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from routes import register_routes

from db import db
from extensions import *
from datetime import datetime as dt

from resources.user_auth import *
from resources.errors import errors

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
    import settings # Import settings here due to conflict on test.py

    app = Flask(__name__)

    if env == "production":
        app.config.from_object('settings.ProductionConfig')
    elif env == "staging":
        app.config.from_object('settings.StagingConfig')
    else:
        app.config.from_object('settings.DevelopmentConfig')

    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        },
    }

    api = Api(app)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    register_extensions(app)
    register_routes(api)

    setup_swagger(app)

    return app

def register_extensions(app):
    logs.init_app(app)
    db.init_app(app)

    return None

def setup_swagger(app):
    from apispec import APISpec
    from apispec.ext.marshmallow import MarshmallowPlugin
    from flask_apispec.extension import FlaskApiSpec

    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Cookery API',
            version='v0.1',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0.0'
        ),
        'APISPEC_SWAGGER_URL': '/api/swagger.json',  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': '/api/swagger'  # URI to access UI of API Doc
    })

    docs = FlaskApiSpec(app)
    docs.register(HelloWorldAPI)
    docs.register(UserSignUpAPI)
    docs.register(UserAuthAPI)

def main():
    app = create_app("dev")
    app.run()

if __name__ == '__main__':
    # from db import db
    # db.init_app(app)
    # initialize_routes(api)
    # app.run(port=5000, debug=True)
    main()
