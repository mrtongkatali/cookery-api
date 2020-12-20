import json
import unittest

from test import BaseCase

from models.user import User, UserProfile
class AuthTest(BaseCase):
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

    @unittest.skip("demonstrating skipping")
    def skip_test_example(self):
        # https://docs.python.org/3.6/library/unittest.html
        pass

    def test_sign_up(self):
        # !!! READ !!!
        # https://medium.com/@AuthorVivek/leveraging-the-power-of-decorators-in-pythons-unit-test-framework-5ae0285d0d27
        # https://docs.python.org/3.6/library/unittest.html#unittest.TestCase.setUpClass
        # https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
        user = self.register_user()
        new_user = self.find_user()

        authorized = new_user.check_password('Abc123!xyz')

        # Test user signup
        self.assertEqual(user.username, new_user.username)
        self.assertEqual(authorized, True)

    @unittest.expectedFailure
    def test_invalid_password(self):
        user = self.register_user()
        new_user = self.find_user()

        authorized = new_user.check_password('123123')

        self.assertEqual(authorized, True)

    def test_create_profile(self):
        user = self.register_user()
        payload = {
            "photoFsRef": "https://google.com",
            "coverPhotoFsRef": "https://google.com",
            "tagline": "Some Tagline",
            "short_bio": "Short Bio",
            "country": "PH",
            "user_id": user.id
        }

        profile = UserProfile(**payload)
        profile.save()

        self.assertEqual(1, profile.id)

    @unittest.expectedFailure
    def test_create_profile_missing_fields(self):
        user = self.register_user()
        payload = {
            "photoFsRef": "https://google.com",
            "coverPhotoFsRef": "https://google.com",
            "tagline": "Some Tagline",
            "user_id": user.id
        }

        profile = UserProfile(**payload)
        profile.save()

        self.assertEqual(1, profile.id)
