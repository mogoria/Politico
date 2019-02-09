import unittest
from app.api.v1.models.political_office_model import PoliticalOffice
from . import BaseTest

class InitOffice:
    """sets mock data to be used for testing"""
    Office = PoliticalOffice()
    office1 = {
        "id":76,
        "type":"type1",
        "name":"office1"
    }
    office2 = {
        "id":22,
        "type":"type2",
        "name":"office2"
    }

class BaseOfficeClass(InitOffice, BaseTest):
    """sets the url path for office endpoints"""
    path = "/api/v1/offices"

class TestOfficeModel(InitOffice, unittest.TestCase):         
    """tests the office model"""
    def test_create_office(self):
        """tests whether office model can create office"""
        self.Office.create_office(** self.office1)
        self.assertEqual(len(self.Office.Offices), 1)
        self.assertEqual(self.Office.Offices[0], self.office1)

    def test_get_all_offices(self):
        """tests whether the office model gets all offices"""
        self.Office.Offices.clear()
        self.Office.create_office(** self.office1)
        self.Office.create_office(** self.office2)
        self.assertEqual(len(self.Office.get_all_offices()), 2)

    def test_get_single_office(self):
        """tests whether the office model can get a specific office"""
        res = self.Office.get_office(22)
        self.assertEqual(res, self.office2)

class TestOfficeStatusCodes(BaseOfficeClass, InitOffice):
    def test_create_office(self):
        """tests the endpoint to create an office"""
        resp = self.post(self.office1)
        self.assertEqual(resp.status_code, 201)

    def test_get_all_offices(self):
        """tests endpoint to get all offices"""
        self.post(self.office2)
        resp = self.get()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['data'][-1], self.office2)

    def test_get_specific_office(self):
        new_office = self.post(self.office2)
        office_id = new_office.json['data'][0]['id']
        resp = self.get_single(office_id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['data'][0], new_office.json['data'][0])

class TestValidation(BaseOfficeClass):
    def test_missing_key(self):
        data = {
            "id":254,
            "":"type2",
            "name":"office2"
        }
        post = self.post(data)
        self.assertEqual(post.status_code, 400)
        print(post.json['error'])
        self.assertTrue(post.json['error'])

    def test_more_keys(self):
        data = {
            "id": 32,
            "name":"office3",
            "type": "type13",
            "extra key": "value"
        }

        post = self.post(data)
        self.assertEqual(post.status_code, 400)
        self.assertIn("incorrect format", post.json["message"])

    def test_get_in_empty_db(self):
        self.assertEqual(self.get().status_code, 404)

    def test_getting_non_existing_id(self):
        self.post(self.office1)
        self.assertTrue(self.get().status_code, 404)
