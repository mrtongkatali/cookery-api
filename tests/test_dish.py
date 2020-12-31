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
        new_dish = Dish.find_by_id(dish.id)

        self.assertEqual(dish.id, new_dish.id)
        self.assertEqual(dish.dish_name, new_dish.dish_name)
        self.assertEqual(dish.cook_minute, new_dish.cook_minute)
        self.assertEqual(dish.cuisine, new_dish.cuisine)
        self.assertEqual(dish.prep_hour, new_dish.prep_hour)
        self.assertEqual(dish.cook_hour, new_dish.cook_hour)
        self.assertEqual(dish.course, new_dish.course)
        self.assertEqual(dish.cook_hour, new_dish.cook_hour)
        self.assertEqual(dish.serving_count, new_dish.serving_count)
        self.assertEqual(dish.user_id, new_dish.user_id)
        self.assertEqual(dish.status, new_dish.status)

    @unittest.expectedFailure
    def test_add_dish_missing_user(self):
        payload = {
        	"cook_minute": 10,
        	"cuisine": 1,
        	"prep_hour": 0,
        	"prep_minute": 10,
        	"cook_hour": 3,
            "course": 1,
            "dish_name": "Chicken Bulanglang",
            "serving_count": 4
        }

        dish = Dish(**payload)
        dish.save()

        self.assertEqual(1, dish.id)

    def test_update_dish(self):
        dish = self.add_dish()
        new_dish = Dish.find_by_id(dish.id)

        payload = {
        	"cuisine": 99,
        	"prep_hour": 99,
        	"prep_minute": 99,
        	"cook_hour": 99,
            "cook_minute": 99,
            "course": 99,
            "dish_name": "Test Me!",
            "serving_count": 99
        }

        new_dish.update(payload)

        updated_dish = Dish.find_by_id(dish.id)

        self.assertEqual(99, updated_dish.cook_minute)
        self.assertEqual(99, updated_dish.cuisine)
        self.assertEqual(99, updated_dish.prep_hour)
        self.assertEqual(99, updated_dish.prep_minute)
        self.assertEqual(99, updated_dish.cook_hour)
        self.assertEqual(99, updated_dish.course)
        self.assertEqual("Test Me!", updated_dish.dish_name)
        self.assertEqual(99, updated_dish.serving_count)
        self.assertEqual(1, updated_dish.status)
