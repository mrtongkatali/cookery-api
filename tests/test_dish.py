import json
import unittest

from test import BaseCase

from models.user import User, UserProfile
from models.dish import Dish

class DishTest(BaseCase):
    def register_user(self):
        payload = {"username": "lexad", "lastname": "D", "firstname": "Lexa", "password":"Abc123!xyz"}

        user = User(**payload)
        user.hash_password()
        user.save()

        return user

    def find_user(self):
        qs = {"username": "lexad"}
        new_user = User.find_by_username(**qs)

        return new_user

    def add_dish(self):
        user = self.register_user()

        payload = {
        	"cook_minute": 10,
        	"cuisine": 1,
        	"prep_hour": 0,
        	"prep_minute": 10,
        	"cook_hour": 3,
            "course": 1,
            "dish_name": "Chicken Bulanglang",
            "serving_count": 4,
            "user_id": 1
        }

        dish = Dish(**payload)
        dish.save()

        return dish

    def test_add_dish(self):
        dish = self.add_dish()

        self.assertEqual(1, dish.id)
