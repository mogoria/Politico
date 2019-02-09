import unittest
import json
from app import create_app
from app.api.v1.models.political_party_model import PoliticalParty
from app.api.v1.views.political_office_route import OFFICE
from app.api.v1.views.political_party_route import PARTY


class BaseTest(unittest.TestCase):
    "base class for test"
    path = "/api/v1"
    def setUp(self):
        """configures the settings to be used to test"""
        self.app = create_app(config_name='testing')
        self.app.testing = True
        self.client = self.app.test_client()

    def post(self, data):
        """returns response from a post request"""
        return self.client.post(path=self.path,
                                data=json.dumps(data), content_type="application/json")

    def get(self):
        """returns response from a get request"""
        return self.client.get(path=self.path, content_type="application/json")

    def get_single(self, id):
        """returns response from get request for a specific id"""
        path = "{}/{}".format(self.path, id)
        return self.client.get(path=path, content_type="application/json")

    def delete(self, id):
        """returns response from a delete request"""
        path = "{}/{}".format(self.path, id)
        return self.client.delete(path, content_type="application/json")

    def tearDown(self):
        """cleans up after test has run"""
        self.app.testing = False
        OFFICE.Offices.clear()
        PARTY.parties.clear()
