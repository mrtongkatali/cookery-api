from constant import *
from serializer import *
from models import *
from settings import *

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object('settings.DevelopmentConfig')

api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Schema
class UserProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserProfile

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    firstname = ma.auto_field()
    lastname = ma.auto_field()

    user_profile = ma.Nested(UserProfileSchema)

# Resource
class UserResource(Resource):
    def get(self):
        one_user = User.query.all()
        return {'users': UserSchema(many=True).dump(one_user)}, 201

    def post(self):
        req = request.get_json(force=True)
        errors = UserValidationSchema().validate(req)

        if errors:
            return ErrorSerializer().dump(dict(message=BAD_REQUEST, errors=errors)), 400
        else:
            user = User.query.filter_by(username=req['username']).first()
            if user:
                return ErrorSerializer().dump(dict(message=INTERNAL_ERROR, errors=['username already exists.'])), 500

            user = User(**req)
            user.hash_password()
            user.save()

            return SuccessSerializer().dump(
                dict(message="Successful.", data=UserSchema().dump(user))
            ), 200

class UserAuthResource(Resource):
    @jwt_required
    def get(self):
        if get_jwt_identity():
            user = User.query.get(get_jwt_identity())
            return dict(data=UserSchema().dump(user)), 200
        else:
            return ErrorSerializer().dump(dict(message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again'])), 401

    def post(self):
        req = request.get_json(force=True)
        user = User.query.filter_by(username=req.get('username')).first()

        if user is not None:
            authorized = user.check_password(req.get('password'))
            if not authorized:
                return ErrorSerializer().dump(dict(message=BAD_REQUEST, errors=['Invalid username or password.'])), 400
            else:
                expires = timedelta(days=7)
                access_token = create_access_token(identity=str(user.id), expires_delta=expires)

                return dict(message="Authenticated", token=access_token), 200
        else:
            return ErrorSerializer().dump(dict(message=BAD_REQUEST, errors=['Invalid username or password.'])), 400

api.add_resource(UserResource, '/user/sign-up', )
api.add_resource(UserAuthResource, '/user/auth', )

# Sample
# class TodoSimple(Resource):
#     def get(self, todo_id):
#         return {'hello': todo_id}, 201
#
#     def post(self):
#         return {'payload': request.get_json(force=True)}
#
# api.add_resource(TodoSimple,
#     '/todo/<string:todo_id>',
#     '/todo'
# )

if __name__ == "__main__":
    app.run(debug=True)

"""
DESIGN DOC

General Overview

PHASE 1:
- Create a web application for sharing homemade cooked meals.
- As a user, I can create an account to the site, then make my own recipe.
- As a user, I can publish my own recipe or make it private
- As a user, my recipe can be peer reviewed and rated by other users
- As a user, I can review or bookmark someone's public recipe
- As a user, I can search a recipe using my available ingredients

PHASE 2:
- As as user, I

Login and Registration


cookeryuser / P@ssw0rd!

TODO LATER:
https://www.youtube.com/watch?v=kRNXKzfYrPU
https://flask-marshmallow.readthedocs.io/en/latest/

"""
