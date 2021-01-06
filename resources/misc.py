import logging
import time

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.dish import Dish
from common.schema import DishSchema
from common.serializer import *

from utils.es import Elastic

class ReIndexAPI(Resource):
    def post(self):
        t0 = time.time()

        page = 1
        size = 100
        count = 0
        hasData = True

        while hasData:
            dish = Dish.get_dish_import(page = page, size = size)

            if len(dish.items) == 0:
                hasData = False
            else:
                count += len(dish.items)
                page += 1

        # dish = Dish.get_dish_import(page = page, size = size)
        t1 = time.time()
        elapse = t1 - t0

        list = {
            "totalDataIndexed": count,
            "time": elapse,
            "totalPagesIndexed": page
        }

        return dict(list=list), 200
