import logging

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.prep_instruction import PrepInstruction
from common.constant import *
from common.serializer import *
from common.schema import PrepInstructionSchema

class PrepInstructionAPI(Resource):
    @jwt_required
    def get(self, instr_id):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again.']), 401, DEFAULT_HEADER

        data = PrepInstruction.find_by_id(instr_id)

        return dict(message="OK", data=PrepInstructionSchema().dump(data)), 200, DEFAULT_HEADER

    @jwt_required
    def post(self):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again.']), 401, DEFAULT_HEADER

        req = request.get_json(force=True)
        errors = InstructionNewSerializer().validate(req)

        if errors:
            return dict(message=BAD_REQUEST, errors=errors), 400, DEFAULT_HEADER

        ins = PrepInstruction.find_last_step(req['dish_id'])
        step_order = 1 if ins is None else ins.step_order + 1

        ins = PrepInstruction(**req)
        ins.step_order = step_order
        ins.main_dish = 1
        ins.status = 1
        ins.save()

        return dict(message="OK", data=PrepInstructionSchema().dump(ins)), 200, DEFAULT_HEADER

    @jwt_required
    def put(self, instr_id):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again.']), 401, DEFAULT_HEADER

        req = request.get_json(force=True)
        errors = InstructionUpdateSerializer().validate(req)

        if errors:
            return dict(message=BAD_REQUEST, errors=errors), 400, DEFAULT_HEADER

        instruction = PrepInstruction.find_by_id(instr_id)

        if not instruction:
            return dict(message=BAD_REQUEST, errors=['Instruction not found.']), 400, DEFAULT_HEADER

        instruction.update(req)

        return dict(message="OK", data=PrepInstructionSchema().dump(instruction)), 200, DEFAULT_HEADER

class RemoveInstructionAPI(Resource):
    @jwt_required
    def post(self, instr_id):
        if not get_jwt_identity():
            return dict(code=CODE_UNAUTHORIZED, message=UNAUTHORIZED_ERROR, errors=['Invalid token. Please try again.']), 401, DEFAULT_HEADER

        instruction = PrepInstruction.find_by_id(instr_id)

        if not instruction:
            return dict(message=BAD_REQUEST, errors=['Instruction not found.']), 400, DEFAULT_HEADER

        instruction.status = 0
        instruction.save()

        return dict(message="Successfully deleted."), 200, DEFAULT_HEADER
