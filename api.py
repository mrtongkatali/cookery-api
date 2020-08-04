from constant import *
from serializer import *
from models import *
from settings import *
from helpers import *

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch, helpers

import csv, json

app = Flask(__name__)
app.config.from_object('settings.DevelopmentConfig')

api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
es = Elasticsearch()

# Schema
class UserProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserProfile

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    firstname = ma.auto_field()
    lastname = ma.auto_field()

    user_profile = ma.Nested(UserProfileSchema)

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

# Resource
class UserSignUpResource(Resource):
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

class UserAuthResource(Resource):
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

class CsvImporterResource(Resource):
    @jwt_required
    def get(self):
        if get_jwt_identity():
            user = User.query.get(get_jwt_identity())
            data = []

            # d = Dish()
            # d.user_id = user.id
            # d.dish_name = "sdf すべての良い男の子は5をします └(^o^)┐"
            # d.main_dish = 13
            # d.course = 1
            # d.cuisine = 1
            # d.save()
            #
            # s = PrepInstruction()
            # s.dish_id = d.id
            # s.description = "how to cook egg"
            # s.step_order = 1
            # s.save()
            #
            # t = Ingredients()
            # t.dish_id = d.id
            # t.amount = 1
            # t.unit = "cup"
            # t.ingredient_name = 'Egg'
            # t.main_dish = 13
            # t.step_order = 1
            # t.save()

            errResults = []
            with open('data/dessert_recipe.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for r in csv_reader:
                    try:
                        main_dish = 13

                        d = Dish()
                        d.user_id = user.id
                        d.dish_name = r['name']
                        d.main_dish = main_dish
                        d.course = 1
                        d.cuisine = 1
                        d.prep_hour = r['prep_time_hour'] if r['prep_time_hour'] else 0
                        d.prep_minute = r['prep_time_min'] if r['prep_time_min'] else 0
                        d.cook_hour = r['cook_time_hour'] if r['cook_time_hour'] else 0
                        d.cook_minute = r['prep_time_min'] if r['prep_time_min'] else 0
                        d.serving_count = r['serving_count'] if r['serving_count'] else 0
                        d.save()

                        instructions = r['instructions'].strip('[').strip(']').split('.,')
                        step_order = 1
                        for desc in instructions:
                            s = PrepInstruction()
                            s.dish_id = d.id
                            s.main_dish = main_dish
                            s.description = desc
                            s.step_order = step_order
                            s.save()
                            step_order += 1

                        rs = str(r['ingredients']).strip(">>").replace("'", '"').replace('None', '""')
                        ingredients = json.loads(f'''{rs}''')

                        step_order = 1
                        for ingr in ingredients:
                            i = Ingredients()
                            i.dish_id = d.id
                            i.amount = ingr['amount']
                            i.unit = ingr['unit']
                            i.ingredient_name = ingr['name']
                            i.main_dish = main_dish
                            i.step_order = step_order

                            i.save()
                            step_order += 1

                        print(f"Inserted {d} - {r['name']}")

                    except Exception as e:
                        errResults.append({"name": r['name'], "error": e})
                        print(f"err in {r['name']}, {e}")

                    print("\n")
                    data.append(r)

            # response = helpers.bulk(elastic, bulk_json_data(data, "employees", "people"))
            print(f"\n Results \n {errResults}")
            return data
        else:
            return ErrorSerializer().dump(dict(message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again'])), 401

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

api.add_resource(UserSignUpResource, '/v1/user/sign-up',)
api.add_resource(UserAuthResource, '/v1/user/auth',)
api.add_resource(CsvImporterResource, '/v1/csv-importer',)

api.add_resource(DishesResource, '/v1/dishes',)

# Sample
# class TodoSimple(Resource):
#     def get(self, todo_id):
#         return {'hello': todo_id}, 201
#
#     def post(self):
#         return {'payload': request.get_json(force=True)}
#
# api.add_resource(TodoSimple,
#     '/todo/<string:todo_id>',
#     '/todo'
# )

if __name__ == "__main__":
    app.run(debug=True)
