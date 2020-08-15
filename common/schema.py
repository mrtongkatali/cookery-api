from ma import ma
from models.user import *
from models.dish import Dish, PrepInstruction
from models.ingredient import Ingredients

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    firstname = ma.auto_field()
    lastname = ma.auto_field()
    isAdmin = ma.auto_field()

    user_profile = ma.Nested("UserProfileSchema")

class UserProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserProfile

class DishSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Dish

    id = ma.auto_field()
    dish_name = ma.auto_field()
    main_dish = ma.auto_field()
    course = ma.auto_field()
    cuisine = ma.auto_field()
    prep_hour = ma.auto_field()
    prep_minute = ma.auto_field()
    cook_hour = ma.auto_field()
    cook_minute = ma.auto_field()
    serving_count = ma.auto_field()
    status = ma.auto_field()

    ingredients = ma.Nested("IngredientSchema", many=True)
    instruction = ma.Nested("PrepInstructionSchema", many=True)

class IngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ingredients

class PrepInstructionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PrepInstruction
