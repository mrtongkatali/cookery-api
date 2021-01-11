import logging

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.dish import Dish
from models.ingredient import Ingredients

from common.constant import *
from common.serializer import *
from common.schema import IngredientSchema, DishSchema

from utils.es import Elastic

es = Elastic("cookery-dish")

class IngredientAPI(Resource):
    @jwt_required
    def get(self, ingr_id):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again.']), 401

        data = Ingredients.find_by_id(ingr_id)

        return dict(message="OK", data=IngredientSchema().dump(data)), 200

    @jwt_required
    def post(self):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again.']), 401

        req = request.get_json(force=True)
        errors = IngredientNewSerializer().validate(req)

        if errors:
            return dict(code=CODE_BAD_REQUEST, message=BAD_REQUEST, errors=errors), 400

        try:
            ins = Ingredients.find_last_step(req['dish_id'])
            step_order = 1 if ins is None else ins.step_order + 1

            ingredient = Ingredients(**req)
            ingredient.step_order = step_order
            ingredient.grocery_item_id = 1 # Set as default 1 for now
            ingredient.main_dish = 1 # Set as default 1 for now
            ingredient.status = 1 # Active as default
            ingredient.save()

            # trigger update es_keywords field on dish
            dish = Dish.find_by_id(req['dish_id'])
            dish.update_es_keywords()

            # index document
            es.index_document(id=req['dish_id'], body=DishSchema().dump(ingredient.dish))

            return dict(message="OK", data=IngredientSchema().dump(ingredient)), 200
        except Exception as e:
            logging.debug(f"[err] update ingredient - {e} => {req}")
            return dict(message=INTERNAL_ERROR, errors=['An error occured. Please try again later.']), 400

    @jwt_required
    def put(self, ingr_id):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again.']), 401

        req = request.get_json(force=True)
        errors = IngredientUpdateSerializer().validate(req)

        if errors:
            return dict(code=CODE_BAD_REQUEST, message=BAD_REQUEST, errors=errors), 400

        try:
            ingredient = Ingredients.find_by_id(ingr_id)

            if not ingredient:
                return dict(code=CODE_BAD_REQUEST, message=BAD_REQUEST, errors=['Ingredient not found.']), 400

            ingredient.update(req)

            # trigger update es_keywords field on dish
            dish = Dish.find_by_id(ingredient.dish.id)
            dish.update_es_keywords()

            # index document
            es.index_document(id=ingredient.dish.id, body=DishSchema().dump(ingredient.dish))

            return dict(message="OK", data=IngredientSchema().dump(ingredient)), 200
        except Exception as e:
            # log the error here
            return dict(message=INTERNAL_ERROR, errors=['An error occured. Please try again later.']), 400

class RemoveIngredientAPI(Resource):
    @jwt_required
    def post(self, ingr_id):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again.']), 401

        ingredient = Ingredients.find_by_id(ingr_id)

        if not ingredient:
            return dict(code=CODE_BAD_REQUEST, message=BAD_REQUEST, errors=['Ingredient not found.']), 400

        ingredient.status = 0
        ingredient.save()

        # trigger update es_keywords field on dish
        dish = Dish.find_by_id(ingredient.dish.id)
        dish.update_es_keywords()

        # index document
        es.index_document(id=ingredient.dish.id, body=DishSchema().dump(ingredient.dish))

        return dict(message="Successfully deleted."), 200
