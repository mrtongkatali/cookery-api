import unittest
import json

import sys
sys.path.append('..')

from app import current_app
from db import db

class SignUpTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client

        with self.app.app_context():
            db.create_all()


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
