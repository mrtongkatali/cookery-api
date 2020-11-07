from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.prep_instruction import PrepInstruction
from common.constant import *
from common.serializer import *
from common.schema import PrepInstructionSchema

class PrepInstructionsResource(Resource):
    @jwt_required
    def get(self):
        if not get_jwt_identity():
            return ErrorSerializer().dump(
                dict(message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again'])
            ), 401, DEFAULT_HEADER

        return "ok"

class PrepInstructionResource(Resource):
    @jwt_required
    def get(self, ingr_id):
        if not get_jwt_identity():
            return ErrorSerializer().dump(
                dict(message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again'])
            ), 401, DEFAULT_HEADER

        data = Ingredients.find_by_id(ingr_id)

        return SuccessSerializer().dump(
            dict(message="OK", data=IngredientSchema().dump(data))
        ), 200

    @jwt_required
    def put(self, ingr_id):
        if not get_jwt_identity():
            return ErrorSerializer().dump(
                dict(message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again'])
            ), 401, DEFAULT_HEADER

        req = request.get_json(force=True)
        errors = InstructionUpdateSerializer().validate(req)

        if errors:
            return ErrorSerializer().dump(
                dict(message=BAD_REQUEST, errors=errors)
            ), 400, DEFAULT_HEADER

        instruction = PrepInstruction.find_by_id(ingr_id)
        if not instruction:
            return ErrorSerializer().dump(
                dict(message=BAD_REQUEST, errors=['Instruction not found.'])
            ), 400, DEFAULT_HEADER

        instruction.update(req)

        return SuccessSerializer().dump(
            dict(message="OK", data=PrepInstructionSchema().dump(instruction))
        ), 200
