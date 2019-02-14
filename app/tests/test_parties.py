import json
from app.api.v1.models.political_party_model import PoliticalParty
from app.api.v1.views.utils import desanitise, sanitise
from . import BaseTest
from . import unittest


class BasePartiesTest(BaseTest):
    """contains mock data and sets the path to parties"""
    path = "/api/v1/parties"

    party_data = {
        "name":"new party",
        "logoUrl":"https://photos/254",
        "hqAddress": "Nairobi"
    }
    party_data2 = {
        "name":"new party2",
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
        created_party = resp.json['party'][0]
        del created_party['id']
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json['party'][0], self.party_data)

    def test_get_single_party(self):
        """tests the endpoint to get a specific party"""
        self.post(self.party_data)
        party = self.post(self.party_data2).json['party'][0]
        response = self.get_single(party.get('id'))
        self.assertEqual(response.status_code, 200)
        found_party = response.json['party'][0]
        del found_party['id']
        self.assertEqual(found_party, self.party_data2)

    def test_delete_party(self):
        """tests endpoint to delete a party"""
        new_party = self.post(self.party_data2)
        party_id = new_party.json['party'][0]["id"]
        response = self.delete(party_id)
        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted successfully", response.json['party'][0]['message'])

    def test_edit_party_name(self):
        """tests endpoint to change name of a party"""
        new_party = self.post(self.party_data2)
        party_id = new_party.json['party'][0]["id"]
        response = self.patch(party_id, {"name":"new name"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("new name", response.json["party"][0]['name'])


    def test_get_all_parties(self):
        """tests endpoint to get all parties"""
        self.post(self.party_data)
        self.post(self.party_data2)
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['parties'][-1], self.party_data)

class TestPartyModel(BaseTest):         
    """tests the party model"""
    Party = PoliticalParty()
    def test_create_office(self):
        """tests whether party model can create offices"""
        self.Parties.clear()
        new_party = self.Party.create_party(** sanitise(BasePartiesTest.party_data))
        new_party = desanitise(new_party)
        self.assertEqual(len(self.Parties), 1)
        self.assertEqual(
            new_party.get('name'),
            BasePartiesTest.party_data.get('name'))

    def test_get_all_parties(self):
        """tests whether the party model gets all parties"""
        self.Parties.clear()
        self.Party.create_party(** sanitise(BasePartiesTest.party_data))
        self.Party.create_party(** sanitise(BasePartiesTest.party_data2))
        self.assertEqual(len(self.Party.get_all_parties()), 2)

    def test_get_party_by_id(self):
        """tests whether the party model can get a specific party by name"""
        new_party = self.Party.create_party(** sanitise(BasePartiesTest.party_data))
        res = self.Party.get_party_by_id(desanitise(new_party).get('id'))
        del res['_id']
        self.assertEqual(desanitise(res), BasePartiesTest.party_data)

    def test_get_party_by_name(self):
        """tests whether the party model can get a specific party by name"""
        new_party = self.Party.create_party(** sanitise(BasePartiesTest.party_data))
        res = self.Party.get_party_by_name(BasePartiesTest.party_data.get('name'))
        self.assertEqual(res, new_party)

    def test_null_if_no_party(self):
        res = self.Party.get_party_by_name("random name")
        self.assertEqual(res, {})

class TestValidation(BasePartiesTest):
    def test_get_empty_db(self):
        response = self.get()
        self.assertTrue(response.status_code, 404)
        self.assertIn("not found", response.json['error'])

    def test_get_non_existent_party(self):
        response = self.get_single(987439)
        self.assertTrue(response.status_code, 404)
        self.assertIn("not found", response.json['error'])

    
    def test_create_existing_party_name(self):
        self.post(self.party_data)
        #repeat request
        response = self.post(self.party_data)
        self.assertTrue(response.status_code, 409)
        self.assertIn("already exists", response.json['error'])

    def test_edit_non_existent_party(self):
        self.post(self.party_data)
        response = self.patch(self.party_data2.get("id"), {"name":"new name"})
        self.assertTrue(response.status_code, 404)

    def test_edit_invalid_key(self):
        self.post(self.party_data)
        response = self.patch(self.party_data.get('id'), {"extra_field":"value"})
        self.assertTrue(400, response.status_code)

    def test_edit_name_with_more_keys(self):
        new_party = self.post(self.party_data2)
        party_id = new_party.json['party'][0]["id"]
        response = self.patch(party_id, self.party_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("incorrect format", response.json['error'])

    def test_edit_with_invalid_name(self):
        new_party = self.post(self.party_data2)
        party_id = new_party.json['party'][0]["id"]
        response = self.patch(party_id, {"name":200})
        self.assertEqual(response.status_code, 400)
        self.assertIn("enter a valid name", response.json['error'])

    def test_create_invalid_party(self):
        invalid_party = {
            "name":"",
            "logoUrl":"https://photos/257",
            "hqAddress": "Somewhere"
        }
        response = self.post(invalid_party)
        self.assertTrue(response.status_code, 400)
        self.assertIn("incorrect format", response.json['error'])

    def test_create_with_few_fields(self):
        response = self.post({"name":"anonymous"})
        self.assertTrue(response.status_code, 400)
        self.assertIn("incorrect format", response.json['error'])

    def test_delete_non_existent_party(self):
        random_partyid = 24983
        response = self.delete(random_partyid)
        self.assertTrue(response.status_code, 404)
        self.assertIn("not found", response.json['error'])
