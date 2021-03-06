import re
from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Range

class UserValidationSchema(Schema):
    username = fields.Str(required=True, validate=Length(max=20))
    firstname = fields.Str(required=True, validate=Length(max=20))
    lastname = fields.Str(required=True, validate=Length(max=20))
    password = fields.Str(required=True, validate=Length(max=60, min=8))

    @validates('password')
    def is_strong_password(self, data):
        if (bool(re.match('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,30})', data)) !=True):
            raise ValidationError("Password is not strong enough!")

class PaginationQSValidator(Schema):
    page = fields.Integer(required=True)
    size = fields.Integer(required=True)
    sort = fields.Str(required=False)
    q = fields.Str(required=False)

class EsQuerySerializer(Schema):
    page = fields.Integer(required=True)
    size = fields.Integer(required=True)
    ingredient_names = fields.Str(required=True)

class DishNewSerializer(Schema):
    dish_name = fields.Str(required=True, validate=Length(max=100))
    main_dish = fields.Integer(required=True)
    course = fields.Integer(required=True)
    cuisine = fields.Integer(required=True)
    prep_hour = fields.Integer(required=True)
    prep_minute = fields.Integer(required=True)
    cook_hour = fields.Integer(required=True)
    cook_minute = fields.Integer(required=True)
    serving_count = fields.Integer(required=True)
    user_id = fields.Integer(required=True)

class DishUpdateSerializer(Schema):
    dish_name = fields.Str(required=True, validate=Length(max=100))
    course = fields.Integer(required=True)
    cuisine = fields.Integer(required=True)
    prep_hour = fields.Integer(required=True)
    prep_minute = fields.Integer(required=True)
    cook_hour = fields.Integer(required=True)
    cook_minute = fields.Integer(required=True)
    serving_count = fields.Integer(required=True)

class IngredientNewSerializer(Schema):
    dish_id = fields.Integer(required=True)
    # grocery_item_id = fields.Integer(required=True)
    # main_dish = fields.Integer(required=True)
    amount = fields.Float(required=True)
    unit = fields.Str(required=True, validate=Length(max=100))
    ingredient_name = fields.Str(required=True, validate=Length(max=100))
    additional_note = fields.Str(required=False, validate=Length(max=1000), allow_none=True)

class IngredientUpdateSerializer(Schema):
    amount = fields.Float(required=True)
    unit = fields.Str(required=True, validate=Length(max=100))
    ingredient_name = fields.Str(required=True, validate=Length(max=100))
    additional_note = fields.Str(required=False, validate=Length(max=1000), allow_none=True)
    step_order = fields.Integer(required=True)

class InstructionNewSerializer(Schema):
    dish_id = fields.Integer(required=True)
    description = fields.Str(required=True)

class InstructionUpdateSerializer(Schema):
    description = fields.Str(required=True, validate=Length(max=1000))
    step_order = fields.Integer(required=True)

class ErrorSerializer(Schema):
    message = fields.String()
    errors = fields.Dict()

class SuccessSerializer(Schema):
    message = fields.String()
    data = fields.Dict()

class InternalError(Schema):
    message = fields.String()

class Error(Schema):
    message = fields.String()
    errors = fields.Dict()

class Success(Schema):
    message = fields.String()
    data = fields.Dict()

class AuthSuccess(Schema):
    token = fields.String()
    message = fields.String()
    data = fields.Dict()

### SCHEMA FOR SWAGGER ###
class DocUserRegistration(Schema):
    username = fields.Str(required=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    password = fields.Str(required=True)

class DocUserLogin(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class DocDishQuery(Schema):
    page = fields.Integer(required=True, default=1)
    size = fields.Integer(required=True, default=20)
    ingredient_names = fields.Str(description="Comma-separated values e.g ingredient_1, ingredient_2, ingredient_3")

class DocAuthHeader(Schema):
    Authorization = fields.Str(required=True, description="Authorization HTTP header with JWT refresh token e.g Authorization: Bearer xxx.xxx.xxx")
