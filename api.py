from constant import *
from serializer import *
from models import *
from settings import *
from helpers import *

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch, helpers

import csv, json

app = Flask(__name__)
app.config.from_object('settings.DevelopmentConfig')

api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
es = Elasticsearch()

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
class UserSignUpResource(Resource):
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

class CsvImporterResource(Resource):
    def get(self):
        data = []
        with open('data/beef_recipe.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for rows in csv_reader:
                data.append(rows)

        # response = helpers.bulk(elastic, bulk_json_data(data, "employees", "people"))
        return data

api.add_resource(UserSignUpResource, '/user/sign-up',)
api.add_resource(UserAuthResource, '/user/auth',)
api.add_resource(CsvImporterResource, '/csv-importer',)

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
