import logging

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.dish import Dish
from common.schema import DishSchema
from common.serializer import *

from utils.es import Elastic

class ReIndexAPI(Resource):
    def post(self):
        logging.info(f"[info] cron - test")
        return "Nickleback"
