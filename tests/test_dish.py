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

    def test_add_dish(self):
        user = self.register_user()
        pass
