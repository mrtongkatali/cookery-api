import unittest
import json

from app import create_app
from db import db

class BaseCase(self):
    self.app = create_app('testing')
    self.client = self.app.test_client

    with self.app.app_context():
        db.create_all()

    # tests = unittest.TestLoader().discover('tests', pattern='*.py')
    # unittest.TextTestRunner(verbosity=1).run(tests)


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
