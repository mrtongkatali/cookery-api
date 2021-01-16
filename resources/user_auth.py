import logging
from datetime import timedelta

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_restful import Resource

from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

from models.user import User, UserProfile
from common.constant import *
from common.serializer import *
from common.schema import UserSchema

@doc(description='Say `Hello World 1234!`', tags=['Test Me'])
class HelloWorldAPI(MethodResource, Resource):
    def get(self):
        '''
        Say `Hello World!`
        '''
        return "Hello World!"

    @use_kwargs(DocUserRegistration, location="json")
    @marshal_with(ErrorSerializer, code=400)
    def post(self, **kwargs):
        '''
        Say `Test!`
        '''
        req = request.get_json(force=True)
        errors = UserValidationSchema().validate(req)
        return dict(message=BAD_REQUEST, errors=errors)

@doc(description='User Registration', tags=['User'])
class UserSignUpAPI(MethodResource, Resource):
    @use_kwargs(DocUserRegistration, location="json")
    @marshal_with(UserSchema, code="200")
    @marshal_with(ErrorSerializer, code=400)
    def post(self, **kwargs):
        '''
        Get method represents a GET API method
        '''
        try:
            req = request.get_json(force=True)
            errors = UserValidationSchema().validate(req)

            if errors:
                return ErrorSerializer().dump(
                    dict(message=BAD_REQUEST, errors=errors)
                ), 400

            if User.find_by_username(**req):
                return ErrorSerializer().dump(
                    dict(message=BAD_REQUEST, errors={"message": "username already exists."})
                ), 400

            user = User(**req)
            user.hash_password()
            user.save()

            return SuccessSerializer().dump(
                dict(message="Ok.", data=UserSchema().dump(user))
            ), 200
        except Exception as e:
            return ErrorSerializer().dump(
                dict(message=INTERNAL_ERROR, errors={"message": "Something went wrong."})
            ), 500

class UserAuthAPI(Resource):
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
            ), 400

        authorized = user.check_password(req.get('password'))

        if not authorized:
            return ErrorSerializer().dump(
                dict(message=BAD_REQUEST, errors=['Invalid username or password.'])
            ), 400

        expires = timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)

        return dict(message="Authenticated", token=access_token, user=UserSchema().dump(user)), 200
