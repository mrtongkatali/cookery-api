import json
import unittest

from test import BaseCase

from models.user import User
class AuthTest(BaseCase):
    @unittest.skip("demonstrating skipping")
    def skip_test_example(self):
        # https://docs.python.org/3.6/library/unittest.html
        pass

    def test_sign_up(self):
        # !!! READ !!!
        # https://medium.com/@AuthorVivek/leveraging-the-power-of-decorators-in-pythons-unit-test-framework-5ae0285d0d27
        # https://docs.python.org/3.6/library/unittest.html#unittest.TestCase.setUpClass
        # https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
        payload = {"username": "lexad", "lastname": "D", "firstname": "Lexa", "password":"Abc123!xyz"}

        user = User(**payload)
        user.hash_password()
        user.save()

        qs = {"username": "lexad"}
        new_user = User.find_by_username(**qs)

        authorized = user.check_password('Abc123!xyz')

        # Test user signup
        self.assertEqual(payload['username'], new_user.username)

    # def test_valid_login(self):
    #     payload = {"username": "lexad"}
    #     new_user = User.find_by_username(**payload)
    #
    #     # authorized = user.check_password('Abc123!xyz')
    #
    #     self.assertEqual(payload['username'], new_user.username)
