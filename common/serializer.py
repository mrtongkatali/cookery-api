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
    fields = fields.Integer(required=False)

class DishUpdateSerializer(Schema):
    dish_name = fields.Str(required=True, validate=Length(max=100))
    course = fields.Integer()
    cuisine = fields.Integer()
    prep_hour = fields.Integer()
    prep_minute = fields.Integer()
    cook_hour = fields.Integer()
    cook_minute = fields.Integer()
    serving_count = fields.Integer()

class ErrorSerializer(Schema):
    message = fields.String()
    errors = fields.Dict()

class SuccessSerializer(Schema):
    message = fields.String()
    data = fields.Dict()
