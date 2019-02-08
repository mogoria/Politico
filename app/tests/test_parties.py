import json
from . import BaseTest



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
        self.assertEqual(self.post(self.party_data).status_code, 201)

    def test_get_single_party(self):
        """tests the endpoint to get a specific party"""
        response = self.get_single(254)
        self.assertEqual(response.status_code, 200)

    def test_delete_party(self):
        """tests endpoint to delete a party"""
        new_party = self.post(self.party_data2)
        party_id = new_party.json['data'][0]["id"]
        response = self.delete(party_id)
        self.assertEqual(response.status_code, 200)

    def test_edit_party_name(self):
        """tests endpoint to change name of a party"""
        new_party = self.post(self.party_data2)
        party_id = new_party.json['data'][0]["id"]
        response = self.patch(party_id, self.party_data2)
        self.assertEqual(response.status_code, 200)

    def test_get_all_parties(self):
        """tests endpoint to get all parties"""
        response = self.get()
        self.assertEqual(response.status_code, 200)
