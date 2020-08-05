from ma import ma

from flask import request
from flask_restful import Resource

from models.dish import *
from common.constant import *
from common.serializer import *

# Schema
class DishSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Dish

    id = ma.auto_field()
    dish_name = ma.auto_field()
    main_dish = ma.auto_field()
    course = ma.auto_field()
    cuisine = ma.auto_field()
    prep_hour = ma.auto_field()
    prep_minute = ma.auto_field()
    cook_hour = ma.auto_field()
    cook_minute = ma.auto_field()
    serving_count = ma.auto_field()
    status = ma.auto_field()

    ingredients = ma.Nested("IngredientSchema", many=True)
    instruction = ma.Nested("PrepInstructionSchema", many=True)

class IngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ingredients

class PrepInstructionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PrepInstruction

class DishesResource(Resource):
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
