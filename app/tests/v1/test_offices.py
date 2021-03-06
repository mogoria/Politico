from app.api.v1.models.political_office_model import PoliticalOffice
from app.api.v1.views.utils import sanitise, desanitise
from . import BaseTest


class InitOffice:
    """sets mock data to be used for testing"""
    Office = PoliticalOffice()
    office1 = {
        "type":"legislative",
        "name":"largeoffice"
    }
    office2 = {
        "type":"federal",
        "name":"big office"
    }
    office3 = {
        "type":"state",
        "name":"massive office"
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
        office = self.Offices[0]
        del office['_id']
        self.assertEqual(self.Offices[0], sanitise(self.office1))

    def test_get_all_offices(self):
        """tests whether the office model gets all offices"""
        self.Offices.clear()
        self.Office.create_office(** sanitise(self.office1))
        self.Office.create_office(** sanitise(self.office2))
        self.assertEqual(len(self.Office.get_all_offices()), 2)

    def test_get_office_by_id(self):
        """tests whether the office model can get a specific office"""
        new_office = self.Office.create_office(** sanitise(self.office1))
        office_id = new_office['_id']
        res = self.Office.get_office_by_id(office_id)
        res = desanitise(res)
        #remove id attribut in order to compare
        del res['id']
        self.assertEqual(res, self.office1)

    def test_get_office_by_name(self):
        """tests whether the office model can get a specific office by name"""
        self.Office.create_office(** sanitise(self.office1))
        res = self.Office.get_office_by_name(self.office1.get('name'))
        del res['_id']
        self.assertEqual(res, sanitise(self.office1))

    def test_null_if_no_office(self):
        """checks whether office model returns null if no office is found"""
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
        last_entry = resp.json['offices'][-1]
        del last_entry['id']
        self.assertEqual(resp.json['offices'][-1], self.office2)

    def test_get_specific_office(self):
        """tests endpoint to get a specific office"""
        new_office = self.post(self.office2)
        office_id = new_office.json['office'][0]['id']
        resp = self.get_single(office_id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['office'][0], new_office.json['office'][0])

class TestValidation(BaseOfficeClass):
    def test_missing_key(self):
        """tests for a response with a missing key"""
        data = {
            "":"type2",
            "name":"office2"
        }
        post = self.post(data)
        self.assertEqual(post.status_code, 400)
        self.assertTrue(post.json['error'])

    def test_more_keys(self):
        """tests for a response with a missing key"""
        data = {
            "name":"office3",
            "type": "type13",
            "extra key": "value"
        }

        post = self.post(data)
        self.assertEqual(post.status_code, 400)
        self.assertIn("incorrect format", post.json["error"])

    def test_get_in_empty_db(self):
        """tests for get in an empty database"""
        self.assertEqual(self.get().status_code, 404)
        self.assertIn("offices not found", self.get().json['error'])

    def test_getting_non_existing_id(self):
        """tests a get request for a non existing id"""
        self.post(self.office1)
        resp = self.get_single(9872938754)
        self.assertEqual(resp.status_code, 404)
        self.assertIn("office not found", resp.json['error'])

    def test_create_existing_office(self):
        """tests creating an existing office"""
        self.post(self.office1)
        resp = self.post(self.office1)
        self.assertEqual(resp.status_code, 409)
        self.assertIn('already exists', resp.json['error'])

    def test_invalid_type(self):
        """tests invalid types"""
        invalid_data = {
            "name":234,
            "type": False
        }
        post = self.post(invalid_data)
        self.assertEqual(post.status_code, 400)
        self.assertIn("Please enter a valid name", post.json['error'])

    def test_invalid_office_type(self):
        """tests for offices with invalid types"""
        office = self.office1
        office['type'] = "random type"
        post = self.post(office)
        self.assertEqual(post.status_code, 400)
        self.assertIn('enter a valid type', post.json['error'])
