import logging

from flask import Flask
from flask_restful_swagger_3 import Api, swagger, get_swagger_blueprint
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
    import settings # Import settings here due to conflict on test.py

    app = Flask(__name__)

    if env == "production":
        app.config.from_object('settings.ProductionConfig')
    elif env == "staging":
        app.config.from_object('settings.StagingConfig')
    else:
        app.config.from_object('settings.DevelopmentConfig')

    servers = [{"url": "http://api-dev-cookery.crazyapp.cloud/"}]
    api = Api(app, version='5', servers=servers, title="APP")

    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    register_extensions(app)
    register_routes(api)

    ## init swagger
    SWAGGER_URL = '/api/doc'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = 'swagger.json'  # Our API url (can of course be a local resource)

    swagger_blueprint = get_swagger_blueprint(
        api.open_api_json,
        swagger_prefix_url=SWAGGER_URL,
        swagger_url=API_URL,
        title='Cookery', version='0.1', servers=servers)

    app.register_blueprint(swagger_blueprint)

    # logger = logging.getLogger("app.access")
    # logging.info('info on app.vue')

    return app

def register_extensions(app):
    logs.init_app(app)
    db.init_app(app)

    return None

def main():
    app = create_app("dev")
    app.run()

if __name__ == '__main__':
    # from db import db
    # db.init_app(app)
    # initialize_routes(api)
    # app.run(port=5000, debug=True)
    main()
