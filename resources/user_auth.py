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

@doc(description='Say `Hello World`', tags=["Test"])
class HelloWorldAPI(MethodResource, Resource):
    def get(self):
        '''
        Say `Hello World!`
        '''
        return "Hello World!"

    # @use_kwargs(DocUserRegistration, location="json")
    # @marshal_with(Error, code=400)
    # def post(self, **kwargs):
    #     '''
    #     Say `Test!`
    #     '''
    #     req = request.get_json(force=True)
    #     errors = UserValidationSchema().validate(req)
    #     return dict(message=BAD_REQUEST, errors=errors)

@doc(description='User Registration', tags=['User'])
class UserSignUpAPI(MethodResource, Resource):
    @use_kwargs(DocUserRegistration)
    @marshal_with(UserSchema, code=200)
    @marshal_with(Error, code=400)
    @marshal_with(InternalError, code=500)
    def post(self, **kwargs):
        '''
        User Registration
        '''
        try:
            req = request.get_json(force=True)
            errors = UserValidationSchema().validate(req)

            if errors:
                return dict(message=BAD_REQUEST, errors=errors), 400

            if User.find_by_username(**req):
                return dict(message=BAD_REQUEST, errors={"message": "username already exists."}), 400

            user = User(**req)
            user.hash_password()
            user.save()

            return dict(message="OK", data=UserSchema().dump(user)), 200
        except Exception as e:
            logging.info("[err] POST UserSignUpAPI :: {kwargs}, {e}")
            return dict(message=INTERNAL_ERROR), 500

@doc(description='User Registration', tags=['Auth'])
class UserAuthAPI(MethodResource, Resource):
    @jwt_required
    @use_kwargs(DocAuthHeader, location=("headers"))
    @marshal_with(AuthSuccess, code=200)
    @marshal_with(Error, code=401)
    @marshal_with(InternalError, code=500)
    def get(self, **kwargs):
        try:
            if not get_jwt_identity():
                return dict(message=UNAUTHORIZED_ERROR, errors={"message": "Invalid credentials."}), 401

            user = User.find_by_id(get_jwt_identity())
            return dict(data=UserSchema().dump(user)), 200
        except Exception as e:
            logging.info("[err] GET UserAuthAPI :: {kwargs}, {e}")
            return dict(message=INTERNAL_ERROR), 500

    @use_kwargs(DocUserLogin)
    @marshal_with(AuthSuccess, code=200)
    @marshal_with(Error, code=400)
    @marshal_with(InternalError, code=500)
    def post(self, **kwargs):
        '''
        User Login
        '''
        try:
            req = request.get_json(force=True)
            user = User.find_by_username(**req)

            if user is None:
                return dict(message=BAD_REQUEST, errors={"message": "Invalid username or password."}), 400

            authorized = user.check_password(req.get('password'))
            if not authorized:
                return dict(message=BAD_REQUEST, errors={"message": "Invalid username or password."}), 400

            expires = timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)

            return dict(message="Authenticated", token=access_token, data=UserSchema().dump(user)), 200
        except Exception as e:
            logging.info("[err] POST UserAuthAPI :: {kwargs}, {e}")
            return dict(message=INTERNAL_ERROR), 500
