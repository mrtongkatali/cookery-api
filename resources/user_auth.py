from datetime import timedelta

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_restful import Resource

from models.user import User, UserProfile
from common.constant import *
from common.serializer import *
from common.schema import UserSchema

class UserSignUp(Resource):
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

class UserAuth(Resource):
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
