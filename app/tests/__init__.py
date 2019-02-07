import unittest
from app import create_app


class BaseTest(unittest.TestCase):
    "base class for test"
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
