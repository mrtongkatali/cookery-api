from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.dish import Dish
from common.constant import *
from common.serializer import *
from common.schema import DishSchema

class DishesResource(Resource):
    @jwt_required
    def get(self):
        if not get_jwt_identity():
            return ErrorSerializer().dump(
                dict(
                    code=CODE_UNAUTHORIZED,
                    message=UNAUTHORIZED_ERROR,
                    errors=['Invalid token. Please try again']
                )
            ), 401, DEFAULT_HEADER

        req = request.args
        errors = PaginationQSValidator().validate(req)

        if errors:
            return ErrorSerializer().dump(
                dict(
                    code=CODE_BAD_REQUEST,
                    message=BAD_REQUEST,
                    errors=errors
                )
            ), 400, DEFAULT_HEADER

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
    def get(self, dish_id):
        if not get_jwt_identity():
            return ErrorSerializer().dump(
                dict(
                    code=CODE_UNAUTHORIZED,
                    message=UNAUTHORIZED_ERROR,
                    errors=['Invalid token. Please try again']
                )
            ), 401, DEFAULT_HEADER

        data = Dish.find_by_id(dish_id)

        # res = Collection(data.ingredients).get_active()
        # app.logger.info(res)

        schema = DishSchema().dump(data)

        # schema['ingredients'] = list(map(
        #     lambda ingr: ingr,
        #     filter(lambda i: i['status'] == 1, schema['ingredients'])
        # ))

        return SuccessSerializer().dump(
            dict(message="ok", data=schema)
        ), 200

    @jwt_required
    def put(self, dish_id):
        if not get_jwt_identity():
            return ErrorSerializer().dump(
                dict(
                    code=CODE_UNAUTHORIZED,
                    message=UNAUTHORIZED_ERROR,
                    errors=['Invalid token. Please try again']
                )
            ), 401, DEFAULT_HEADER

        req = request.get_json(force=True)
        errors = DishUpdateSerializer().validate(req)

        if errors:
            return ErrorSerializer().dump(
                dict(
                    code=CODE_BAD_REQUEST,
                    message=BAD_REQUEST,
                    errors=errors
                )
            ), 400, DEFAULT_HEADER

        dish = Dish.find_by_id(dish_id)

        if not dish:
            return ErrorSerializer().dump(dict(code=CODE_BAD_REQUEST, message=BAD_REQUEST, errors=['Dish not found.'])), 400

        dish.update(req)

        return SuccessSerializer().dump(
            dict(message="OK", data=DishSchema().dump(dish))
        ), 200
