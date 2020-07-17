from constant import SECRET_KEY, BAD_REQUEST, INTERNAL_ERROR

from flask import Flask, request
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

from manage import User, UserProfile
from validation import UserValidationSchema, ErrorSerializer

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cookeryuser:P@ssw0rd!@localhost:3306/cookerydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

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
                return ErrorSerializer().dump(dict(message=INTERNAL_ERROR, errors=['username already exists'])), 500

            return "ok"

api.add_resource(UserResource,
    '/user',
)

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
