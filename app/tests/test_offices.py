import unittest
from app.api.v1.models.political_office_model import PoliticalOffice
from . import BaseTest
from app.api.v1.views.utils import sanitise, desanitise

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

class TestOfficeModel(BaseOfficeClass):         
    """tests the office model"""
    def test_create_office(self):
        """tests whether office model can create office"""
        self.Office.create_office(** sanitise(self.office1))
        self.assertEqual(len(self.Offices), 1)
        self.assertEqual(self.Offices[0], sanitise(self.office1))

    def test_get_all_offices(self):
        """tests whether the office model gets all offices"""
        self.Offices.clear()
        self.Office.create_office(** sanitise(self.office1))
        self.Office.create_office(** sanitise(self.office2))
        self.assertEqual(len(self.Office.get_all_offices()), 2)

    def test_get_office_by_id(self):
        """tests whether the office model can get a specific office"""
        self.Office.create_office(** sanitise(self.office1))
        res = self.Office.get_office_by_id(self.office1.get('id'))
        res = desanitise(res)
        self.assertEqual(res, self.office1)

    def test_get_office_by_name(self):
        """tests whether the office model can get a specific office by name"""
        self.Office.create_office(** sanitise(self.office1))
        res = self.Office.get_office_by_name(self.office1.get('name'))
        self.assertEqual(res, sanitise(self.office1))

    def test_null_if_no_office(self):
        res = self.Office.get_office_by_name("random name")
        self.assertEqual(res, {})

class TestOfficeStatusCodes(BaseOfficeClass, InitOffice):
    def test_create_office(self):
        """tests the endpoint to create an office"""
        self.Offices.clear()
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
        self.assertIn("incorrect format", post.json["error"])

    def test_get_in_empty_db(self):
        self.assertEqual(self.get().status_code, 404)
        self.assertIn("offices not found", self.get().json['error'])

    def test_getting_non_existing_id(self):
        self.post(self.office1)
        resp = self.get_single(9872938754)
        self.assertTrue(resp.status_code, 404)
        self.assertIn("office not found", resp.json['error'])

    def test_create_existing_office(self):
        self.post(self.office1)
        resp = self.post(self.office1)
        self.assertTrue(resp.status_code, 409)
        self.assertIn('already exists', resp.json['error'])

    def test_invalid_type(self):
        invalid_data = {
            "id":"123",
            "name":234,
            "type": False
        }
        post = self.post(invalid_data)
        self.assertEqual(post.status_code, 400)
        self.assertIn("incorrect format", post.json['error'])

