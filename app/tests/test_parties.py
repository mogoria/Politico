from . import BaseTest
import json


class BasePartiesTest(BaseTest):
    path = "/api/v1/parties"

    party_data = {
            "name":"new party",
            "id":254,
            "photoUrl":"https://photos/254",
            "hqAddress": "Nairobi"
        }
    party_data2 = {
            "name":"new party2",
            "id":257,
            "logoUrl":"https://photos/257",
            "hqAddress": "Somewhere"
        }
        
    
class TestPartiesStatusCodes(BasePartiesTest):

    def test_create_party(self):
        self.assertTrue(self.post(self.party_data).status_code, 201)

    def test_get_single_party(self):
        pass

    def test_delete_party(self):
        pass

    def test_edit_party_name(self):
        pass

    def test_get_all_parties(self):
        pass

