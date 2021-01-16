from flask_restful_swagger_3 import Schema

class EmailModel(Schema):
    type = 'string'
    format = 'email'


class KeysModel(Schema):
    type = 'string'


class SuperUserModel(Schema):
    type = 'object'
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64',
        },
    }
    required = ['id']


class UserModel(SuperUserModel):
    properties = {
        'name': {
            'type': 'string'
        },
        'mail': EmailModel,
        'keys': KeysModel.array(),
        'user_type': {
            'type': 'string',
            'enum': ['admin', 'regular'],
            'nullable': 'true'
        },
        'password': {
            'type': 'string',
            'format': 'password',
            'load_only': 'true'
        }
    }
    required = ['name']

class ErrorModel(Schema):
    type = 'object'
    properties = {
        'message': {
            'type': 'string'
        }
    }

class CategorySchema(Schema):
    type = "object"
    properties = {"id": {"type": "string"}, "name": {"type": "string"}}
    required = ["name"]


class ProductSchema(Schema):
    type = "object"
    properties = {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "picture": {"type": "string", "nullable": "true"},
        "unit_price": {"type": "number"},
        "unit": {"type": "string"},
        "quantity": {"type": "number"},
        "category": CategorySchema,
    }
    required = ["name", "unit_price", "quantity", "category"]


class TypeSchema(Schema):
    type = "string"
    default = "admin"
    enum = ["admin", "regular"]
