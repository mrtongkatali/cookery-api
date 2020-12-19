import logging
from datetime import timedelta

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_restful import Resource

from models.user import User, UserProfile
from common.constant import *
from common.serializer import *
from common.schema import UserSchema

class HelloWorldResource(Resource):
    def get(self):
        return "Hello World from the other side.."

class UserSignUpResource(Resource):
    def post(self):
        req = request.get_json(force=True)
        errors = UserValidationSchema().validate(req)

        if errors:
            return ErrorSerializer().dump(
                dict(message=BAD_REQUEST, errors=errors)
            ), 400, DEFAULT_HEADER

        if User.find_by_username(**req):
            return ErrorSerializer().dump(
                dict(message=BAD_REQUEST, errors=['username already exists.'])
            ), 400, DEFAULT_HEADER

        user = User(**req)
        user.hash_password()
        user.save()

        return SuccessSerializer().dump(
            dict(message="Ok.", data=UserSchema().dump(user))
        ), 200

class UserAuthResource(Resource):
    @jwt_required
    def get(self):
        if not get_jwt_identity():
            return ErrorSerializer().dump(dict(message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again'])), 401

        user = User.find_by_id(get_jwt_identity())
        return dict(data=UserSchema().dump(user)), 200

    def post(self):
        req = request.get_json(force=True)
        user = User.find_by_username(**req)

        # logger = logging.getLogger("app.access")
        # logging.info(user.username)

        if user is None:
            return ErrorSerializer().dump(
                dict(message=BAD_REQUEST, errors=['Invalid username or password.'])
            ), 400, DEFAULT_HEADER

        authorized = user.check_password(req.get('password'))

        if not authorized:
            return ErrorSerializer().dump(
                dict(message=BAD_REQUEST, errors=['Invalid username or password.'])
            ), 400, DEFAULT_HEADER

        expires = timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)

        return dict(message="Authenticated", token=access_token, user=UserSchema().dump(user)), 200
