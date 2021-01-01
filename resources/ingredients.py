from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.ingredient import Ingredients
from common.constant import *
from common.serializer import *
from common.schema import IngredientSchema

class IngredientAPI(Resource):
    @jwt_required
    def get(self, ingr_id):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again.']), 401, DEFAULT_HEADER

        data = Ingredients.find_by_id(ingr_id)

        return dict(message="OK", data=IngredientSchema().dump(data)), 200, DEFAULT_HEADER

    @jwt_required
    def post(self):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again.']), 401, DEFAULT_HEADER

        req = request.get_json(force=True)
        errors = IngredientNewSerializer().validate(req)

        if errors:
            return dict(code=CODE_BAD_REQUEST, message=BAD_REQUEST, errors=errors), 400, DEFAULT_HEADER

        try:
            ingredient = Ingredients(**req)
            ingredient.grocery_item_id = 1 # Set as default 1 for now
            ingredient.main_dish = 1 # Set as default 1 for now
            ingredient.status = 1 # Active as default
            ingredient.save()

            return dict(message="OK", data=IngredientSchema().dump(ingredient)), 200, DEFAULT_HEADER
        except Exception as e:
            # log the error here
            return dict(message=INTERNAL_ERROR, errors=['An error occured. Please try again later.']), 400, DEFAULT_HEADER

    @jwt_required
    def put(self, ingr_id):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again.']), 401, DEFAULT_HEADER

        req = request.get_json(force=True)
        errors = IngredientUpdateSerializer().validate(req)

        if errors:
            return dict(code=CODE_BAD_REQUEST, message=BAD_REQUEST, errors=errors), 400, DEFAULT_HEADER

        try:
            ingredient = Ingredients.find_by_id(ingr_id)

            if not ingredient:
                return dict(code=CODE_BAD_REQUEST, message=BAD_REQUEST, errors=['Ingredient not found.']), 400, DEFAULT_HEADER

            ingredient.update(req)

            return dict(message="OK", data=IngredientSchema().dump(ingredient)), 200, DEFAULT_HEADER
        except Exception as e:
            # log the error here
            return dict(message=INTERNAL_ERROR, errors=['An error occured. Please try again later.']), 400, DEFAULT_HEADER

class RemoveIngredientAPI(Resource):
    @jwt_required
    def post(self, ingr_id):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again.']), 401, DEFAULT_HEADER

        ingredient = Ingredients.find_by_id(ingr_id)

        if not ingredient:
            return dict(code=CODE_BAD_REQUEST, message=BAD_REQUEST, errors=['Ingredient not found.']), 400, DEFAULT_HEADER

        ingredient.status = 0
        ingredient.save()

        return dict(message="Successfully deleted."), 200, DEFAULT_HEADER
