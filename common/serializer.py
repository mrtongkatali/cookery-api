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
    course = fields.Integer(required=True)
    cuisine = fields.Integer(required=True)
    prep_hour = fields.Integer(required=True)
    prep_minute = fields.Integer(required=True)
    cook_hour = fields.Integer(required=True)
    cook_minute = fields.Integer(required=True)
    serving_count = fields.Integer(required=True)

class IngredientUpdateSerializer(Schema):
    amount = fields.Str(required=True, validate=Length(max=20))
    unit = fields.Integer(required=True)
    ingredient_id = fields.Integer(required=True)
    ingredient_name = fields.Integer(required=True)
    step_order = fields.Integer(required=True)

    # id = db.Column(db.Integer, primary_key=True)
    # dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    # amount = db.Column(db.String(20))
    # unit = db.Column(db.String(20))
    # ingredient_id = db.Column(db.Integer)
    # ingredient_name = db.Column(db.String(200)) # for will be converted to just id after migration
    # main_dish = db.Column(db.Integer) # for tracking, can be deleted after migration
    # step_order = db.Column(db.Integer)

class ErrorSerializer(Schema):
    message = fields.String()
    errors = fields.Dict()

class SuccessSerializer(Schema):
    message = fields.String()
    data = fields.Dict()
