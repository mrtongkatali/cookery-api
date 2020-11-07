from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.ingredient import Ingredients
from common.constant import *
from common.serializer import *
from common.schema import IngredientSchema

class PrepInstructionsResource(Resource):
    @jwt_required
    def get(self):
        if not get_jwt_identity():
            return ErrorSerializer().dump(
                dict(message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again'])
            ), 401, DEFAULT_HEADER

        return "ok"

class PrepInstructionResource(Resource):
    @jwt_required
    def get(self, ingr_id):
        if not get_jwt_identity():
            return ErrorSerializer().dump(
                dict(message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again'])
            ), 401, DEFAULT_HEADER

        data = Ingredients.find_by_id(ingr_id)

        return SuccessSerializer().dump(
            dict(message="OK", data=IngredientSchema().dump(data))
        ), 200

    @jwt_required
    def put(self, ingr_id):
        if not get_jwt_identity():
            return ErrorSerializer().dump(
                dict(message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again'])
            ), 401, DEFAULT_HEADER

        req = request.get_json(force=True)
        errors = IngredientUpdateSerializer().validate(req)

        if errors:
            return ErrorSerializer().dump(
                dict(message=BAD_REQUEST, errors=errors)
            ), 400, DEFAULT_HEADER

        ingredient = Ingredients.find_by_id(ingr_id)
        if not ingredient:
            return ErrorSerializer().dump(
                dict(message=BAD_REQUEST, errors=['Ingredient not found.'])
            ), 400, DEFAULT_HEADER

        ingredient.update(req)

        return SuccessSerializer().dump(
            dict(message="OK", data=IngredientSchema().dump(ingredient))
        ), 200
