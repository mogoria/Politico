from app.api.v2.models.party_model import Party
from app.utils.database import init_db
from . import BaseTestModel


class TestPartyModel(BaseTestModel):
    def setUp(self):
        super().setUp()
        self.data1 = dict(name="President", logourl="logo.com/23", hqaddress="Nairobi")
        self.data2 = dict(name="Governor", logourl="logo.com/22", hqaddress="Mombasa")
        self.invalid_data = dict(name="Governor", logourl="logo.com/2", hqaddress="Kisumu")

    def test_create_party(self):
        party = Party(** self.data1)
        new_party = party.add_party()
        self.assertEqual(new_party, self.data1)

    def test_get_party_by_name(self):
        party = Party(** self.data1)
        party.add_party()

        name = self.data1.get('name')
        new_party = Party.get_party_by_name(name)

        new_party = self.sortnstrip(new_party)
        party_details = self.sortnstrip(self.data1)
    
        self.assertEqual(party_details, new_party)

    def test_get_all_parties(self):
        party1 = Party(** self.data1)
        party2 = Party(** self.data2)
        party1.add_party()
        party2.add_party()

        parties = Party.get_all_parties()
        self.assertTrue(len(parties), 2)

    def test_get_party_id_from_name(self):
        party = Party(** self.data1)
        party.add_party()
        
        party_id = Party.get_party_id_from_name(self.data1.get('name'))
        self.assertEqual(party_id, 1)

    def tearDown(self):
        Party.close()
        init_db.db_refresh()
