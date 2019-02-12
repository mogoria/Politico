import json
from app.api.v1.models.political_party_model import PoliticalParty
from . import BaseTest
from . import unittest


class BasePartiesTest(BaseTest):
    """contains mock data and sets the path to parties"""
    path = "/api/v1/parties"

    party_data = {
        "name":"new party",
        "id":254,
        "logoUrl":"https://photos/254",
        "hqAddress": "Nairobi"
    }
    party_data2 = {
        "name":"new party2",
        "id":257,
        "logoUrl":"https://photos/257",
        "hqAddress": "Somewhere"
    }
    def patch(self, party_id, data):
        """makes a patch request and returns response,
        uses path from base party class"""
        path = "{}/{}/name".format(self.path, party_id)
        return self.client.patch(path, data=json.dumps(data), content_type="application/json")

class TestPartiesStatusCodes(BasePartiesTest):

    def test_create_party(self):
        """tests endpoint to create a party"""
        resp = self.post(self.party_data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json['data'][0], self.party_data)

    def test_get_single_party(self):
        """tests the endpoint to get a specific party"""
        self.post(self.party_data)
        self.post(self.party_data2)
        response = self.get_single(self.party_data.get('id'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['data'][0], self.party_data)

    def test_delete_party(self):
        """tests endpoint to delete a party"""
        new_party = self.post(self.party_data2)
        party_id = new_party.json['data'][0]["id"]
        response = self.delete(party_id)
        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted successfully", response.json['data'][0]['message'])

    def test_edit_party_name(self):
        """tests endpoint to change name of a party"""
        new_party = self.post(self.party_data2)
        party_id = new_party.json['data'][0]["id"]
        response = self.patch(party_id, self.party_data2)
        self.assertEqual(response.status_code, 200)
        self.assertIn("updated successfully", response.json["data"][0]["message"])

    def test_get_all_parties(self):
        """tests endpoint to get all parties"""
        self.post(self.party_data)
        self.post(self.party_data2)
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['data'][-1], self.party_data)

class TestPartyModel(unittest.TestCase):         
    """tests the party model"""
    Party = PoliticalParty()
    def test_create_office(self):
        """tests whether party model can create offices"""
        self.Party.parties.clear()
        self.Party.create_party(** BasePartiesTest.party_data)
        self.assertEqual(len(self.Party.parties), 1)
        self.assertEqual(self.Party.parties.get(254), BasePartiesTest.party_data)

    def test_get_all_parties(self):
        """tests whether the party model gets all parties"""
        self.Party.parties.clear()
        self.Party.create_party(** BasePartiesTest.party_data)
        self.Party.create_party(** BasePartiesTest.party_data2)
        self.assertEqual(len(self.Party.get_all_parties()), 2)

    def test_get_party_by_id(self):
        """tests whether the party model can get a specific party by name"""
        res = self.Party.get_party_by_id(BasePartiesTest.party_data.get('id'))
        self.assertEqual(res, BasePartiesTest.party_data)

    def test_get_party_by_name(self):
        """tests whether the party model can get a specific party by name"""
        res = self.Party.get_party_by_name(BasePartiesTest.party_data.get('name'))
        self.assertEqual(res, BasePartiesTest.party_data)

    def test_null_if_no_party(self):
        res = self.Party.get_party_by_name("random name")
        self.assertEqual(res, {})

class TestValidation(BasePartiesTest):
    def test_get_empty_db(self):
        response = self.get()
        self.assertTrue(response.status_code, 404)
        self.assertIn("not found", response.json['error'])

    def test_get_non_existent_party(self):
        response = self.get_single(self.party_data.get('id'))
        self.assertTrue(response.status_code, 404)

    def test_create_existing_party_id(self):
        self.post(self.party_data)
        response = self.post(self.party_data)
        self.assertTrue(response.status_code, 409)
        self.assertIn("already exists", response.json['error'])
    
    def test_create_existing_party_name(self):
        self.post(self.party_data)
        #only change the id
        test_data = self.party_data
        test_data['id'] = 234
        print(test_data)
        response = self.post(test_data)
        self.assertTrue(response.status_code, 409)
        self.assertIn("already exists", response.json['error'])

    def test_edit_non_existent_party(self):
        self.post(self.party_data)
        response = self.patch(self.party_data2.get("id"), {"name":"new name"})
        self.assertTrue(response.status_code, 404)

    def test_edit_invalid_request(self):
        self.post(self.party_data)
        response = self.patch(self.party_data.get('id'), {"extra_field":"value"})
        self.assertTrue(400, response.status_code)

    def test_create_invalid_party(self):
        invalid_party = {
            "name":"",
            "id":257,
            "logoUrl":"https://photos/257",
            "hqAddress": "Somewhere"
        }
        response = self.post(invalid_party)
        self.assertTrue(response.status_code, 400)
        self.assertIn("incorrect format", response.json['error'])

    def test_create_with_few_fields(self):
        response = self.post({"name":"Tukmen"})
        self.assertTrue(response.status_code, 400)
        self.assertIn("incorrect format", response.json['error'])

    def test_delete_non_existent_party(self):
        self.post(self.party_data)
        response = self.delete(self.party_data2.get("id"))
        self.assertTrue(response.status_code, 404)
        self.assertIn("not found", response.json['error'])
