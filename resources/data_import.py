from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from models.user import User
from common.constant import *
from common.serializer import *

import csv, json

class DishImport(Resource):
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
                    # try:
                    #     main_dish = 13
                    #
                    #     d = Dish()
                    #     d.user_id = user.id
                    #     d.dish_name = r['name']
                    #     d.main_dish = main_dish
                    #     d.course = 1
                    #     d.cuisine = 1
                    #     d.prep_hour = r['prep_time_hour'] if r['prep_time_hour'] else 0
                    #     d.prep_minute = r['prep_time_min'] if r['prep_time_min'] else 0
                    #     d.cook_hour = r['cook_time_hour'] if r['cook_time_hour'] else 0
                    #     d.cook_minute = r['prep_time_min'] if r['prep_time_min'] else 0
                    #     d.serving_count = r['serving_count'] if r['serving_count'] else 0
                    #     d.save()
                    #
                    #     instructions = r['instructions'].strip('[').strip(']').split('.,')
                    #     step_order = 1
                    #     for desc in instructions:
                    #         s = PrepInstruction()
                    #         s.dish_id = d.id
                    #         s.main_dish = main_dish
                    #         s.description = desc
                    #         s.step_order = step_order
                    #         s.save()
                    #         step_order += 1
                    #
                    #     rs = str(r['ingredients']).strip(">>").replace("'", '"').replace('None', '""')
                    #     ingredients = json.loads(f'''{rs}''')
                    #
                    #     step_order = 1
                    #     for ingr in ingredients:
                    #         i = Ingredients()
                    #         i.dish_id = d.id
                    #         i.amount = ingr['amount']
                    #         i.unit = ingr['unit']
                    #         i.ingredient_name = ingr['name']
                    #         i.main_dish = main_dish
                    #         i.step_order = step_order
                    #
                    #         i.save()
                    #         step_order += 1
                    #
                    #     print(f"Inserted {d} - {r['name']}")
                    #
                    # except Exception as e:
                    #     errResults.append({"name": r['name'], "error": e})
                    #     print(f"err in {r['name']}, {e}")
                    #
                    # print("\n")
                    data.append(r)

            # response = helpers.bulk(elastic, bulk_json_data(data, "employees", "people"))
            # print(f"\n Results \n {errResults}")
            return data
        else:
            return ErrorSerializer().dump(dict(message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again'])), 401
