from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from settings import *
from resources.user_auth import *

app = Flask(__name__)
app.config.from_object('settings.DevelopmentConfig')

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

api.add_resource(UserSignUpResource, '/v1/user/sign-up',)
api.add_resource(UserAuthResource, '/v1/user/auth',)

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
