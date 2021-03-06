import logging

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

from models.dish import Dish
from common.constant import *
from common.serializer import *
from common.schema import DishSchema

from utils.es import Elastic

es = Elastic("cookery-dish")

@doc(description="Full-text search", tags=["Dish"])
class DishesElasticAPI(MethodResource, Resource):
    @jwt_required
    @use_kwargs(DocDishQuery)
    @use_kwargs(DocAuthHeader, location=("headers"))
    @marshal_with(Success, code=200)
    @marshal_with(Error, code=400)
    @marshal_with(InternalError, code=500)
    def post(self, **kwargs):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors={"message": "Invalid credentials."}), 401

        req = request.get_json(force=True)
        errors = EsQuerySerializer().validate(req)
        if errors:
            return dict(code=CODE_BAD_REQUEST, message=BAD_REQUEST, errors=errors), 400

        query = "*" if req['ingredient_names'] is None else req['ingredient_names']

        body = {
            "from": req['page'],
            "size": req['size'],
            "sort": [
                {"id": {"order": "desc"}}
            ],
            "query": {}
        }
        if req['ingredient_names'] is None:
            body['query']['match_all'] = {}
        else:
            # body['query']['query_string'] = {
            #     "query": query,
            # }
            must = []
            for v in req['ingredient_names'].split(","):
                must.append({ "match": { "es_keywords": v.strip() }})

            body["query"] = { "bool": { "must": must } }
            # body['query']['nested'] = {
            #     "path": "ingredients",
            #     "query": {
            #         # "query_string": {
            #         #     "query": q
            #         # }
            #         "terms": {
            #             ""
            #         }
            #     }
            # }
            # body['query']['nested'] = {
            #     "path": "ingredients",
            #     "query": {
            #         "bool": {
            #             "must": [
            #                 { "match": { "ingredients.ingredient_name": "flour" }},
            #                 { "match": { "ingredients.ingredient_name": "sugar" }}
            #             ]
            #         }
            #     }
            # }

        data = []
        dishes = es.search_data(body=body)

        if len(dishes['hits']['hits']) > 0:
            for source in dishes['hits']['hits']:
                dish = source['_source']
                data.append(dish)

        list = {
            "list": data,
            "count": len(dishes['hits']['hits']),
            "total": dishes['hits']['total']['value']
        }

        return dict(message="OK", data=list), 200

class DishesAPI(Resource):
    @jwt_required
    def get(self):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors={"message": "Invalid credentials."}), 401

        req = request.args
        errors = PaginationQSValidator().validate(req)

        if errors:
            return dict(code=CODE_BAD_REQUEST, message=BAD_REQUEST, errors=errors), 400

        dish = Dish.get_all_dishes(**req)
        list = {
            "list": DishSchema(many=True).dump(dish.items),
            "count": len(dish.items),
            "total": dish.total
        }

        return dict(message="OK", data=list), 200

class DishAPI(Resource):
    @jwt_required
    def get(self, dish_id):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors={"message": "Invalid credentials."}), 401

        data = Dish.find_by_id(dish_id)

        # res = Collection(data.ingredients).get_active()
        # app.logger.info(res)

        schema = DishSchema().dump(data)

        # schema['ingredients'] = list(map(
        #     lambda ingr: ingr,
        #     filter(lambda i: i['status'] == 1, schema['ingredients'])
        # ))

        return dict(message="OK", data=schema), 200

    @jwt_required
    def post(self):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors={"message": "Invalid credentials."}), 401

        req = request.get_json(force=True)
        errors = DishNewSerializer().validate(req)

        if errors:
            return dict(code=CODE_BAD_REQUEST, message=BAD_REQUEST, errors=errors), 400

        dish = Dish(**req)
        dish.save()

        # index document
        obj = Dish.find_by_id(dish.id)
        es.create(id=obj.id, body=DishSchema().dump(obj))

        return dict(message="OK", data=DishSchema().dump(dish)), 200

    @jwt_required
    def put(self, dish_id):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors={"message": "Invalid credentials."}), 401

        req = request.get_json(force=True)
        errors = DishUpdateSerializer().validate(req)

        if errors:
            return dict(code=CODE_BAD_REQUEST, message=BAD_REQUEST, errors=errors), 400

        dish = Dish.find_by_id(dish_id)

        if not dish:
            return dict(code=CODE_BAD_REQUEST, message=BAD_REQUEST, errors=['Dish not found.']), 400

        dish.update(req)
        es.index_document(id=dish.id, body=DishSchema().dump(dish))

        return dict(message="OK", data=DishSchema().dump(dish)), 200

class RemoveDishAPI(Resource):
    @jwt_required
    def post(self, dish_id):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors={"message": "Invalid credentials."}), 401

        dish = Dish.find_by_id(dish_id)

        if not dish:
            return dict(code=CODE_BAD_REQUEST, message=BAD_REQUEST, errors=['Dish not found.']), 200

        dish.status = 0
        dish.save()

        # index dish
        es.index_document(id=dish.id, body=DishSchema().dump(dish))

        return dict(message="Successfully deleted."), 200
