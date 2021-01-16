import logging
import time

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.dish import Dish
from common.schema import DishSchema
from common.serializer import *

from utils.es import Elastic
es = Elastic("cookery-dish")

class SyncESKewordsAPI(Resource):
    def post(self):
        # trigger update for es_keywords field on dish
        try:
            page = 1
            size = 1000
            dishes = Dish.get_dish_import(page=page, size=size)

            for d in dishes.items:
                d.update_es_keywords()

            return dict(message="Successful"), 200

        except Exception as e:
            logging.debug(f"[err] Sync es keywords => {e}")

class ReIndexAPI(Resource):
    def post(self):
        t0 = time.time()

        page = 1
        size = 1000
        count = 0
        hasData = True

        while hasData:
            dishes = Dish.get_dish_import(page=page, size=size)

            if len(dishes.items) == 0:
                hasData = False
            else:
                es.bulk_index(body=dishes.items)
                count += len(dishes.items)
                page += 1

        t1 = time.time()
        elapse = t1 - t0

        list = {
            "totalDataIndexed": count,
            "time": elapse,
            "totalPagesIndexed": page
        }

        return dict(list=list), 200
