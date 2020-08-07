from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.dish import Dish
from common.constant import *
from common.serializer import *
from common.schema import DishSchema

class DishesResource(Resource):
    def get(self):
        req = request.args
        errors = PaginationQSValidator().validate(req)

        if errors:
            return ErrorSerializer().dump(dict(message=BAD_REQUEST, errors=errors)), 400
        else:
            dish = Dish.get_all_dishes(**req)
            list = {
                "list": DishSchema(many=True).dump(dish.items),
                "count": len(dish.items),
                "total": dish.total
            }

            return SuccessSerializer().dump(
                dict(message="OK", data=list)
            ), 200

class DishResource(Resource):
    @jwt_required
    def patch(self, dish_id):
        if not get_jwt_identity(): return ErrorSerializer().dump(dict(message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again'])), 401
        else:
            req = request.get_json(force=True)
            print(req)
            errors = DishUpdateSerializer().validate(req)

            if errors: return ErrorSerializer().dump(dict(message=BAD_REQUEST, errors=errors)), 400
            else:
                return "asda"

    @jwt_required
    def get(self, dish_id):
        if not get_jwt_identity(): return ErrorSerializer().dump(dict(message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again'])), 401
        else:
            data = Dish.find_by_id(dish_id)

            return SuccessSerializer().dump(
                dict(message="OK", data=DishSchema().dump(data))
            ), 200
