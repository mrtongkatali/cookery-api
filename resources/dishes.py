from flask import request
from flask_restful import Resource

from models.dish import Dish
from common.constant import *
from common.serializer import *
from common.schema import DishSchema

class Dishes(Resource):
    def get(self):
        req = request.args
        errors = PaginationQSValidator().validate(req)

        if errors:
            return ErrorSerializer().dump(dict(message=BAD_REQUEST, errors=errors)), 400
        else:
            dish = Dish.query \
                .order_by(Dish.id.desc()) \
                .paginate(int(req["page"]),int(req["size"]),error_out=False)

            list = {
                "list": DishSchema(many=True).dump(dish.items),
                "total": dish.total
            }

            return SuccessSerializer().dump(
                dict(message="Successful.", data=list)
            ), 200
