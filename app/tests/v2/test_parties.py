from app.api.v2.models.party_model import Party
from . import BaseTestModel


class TestPartyModel(BaseTestModel):
    def setUp(self):
        super().setUp()
        self.invalid_party_data = dict(name="Governor", logourl="logo.com/2",
                                       hqaddress="Kisumu")

    def test_create_party(self):
        new_party = self.create_party(self.party_data)

        self.assertEqual(new_party, self.party_data)

    def test_get_party_by_name(self):
        self.create_party(self.party_data)

        name = self.party_data.get('name')
        new_party = Party.get_party_by_name(name)

        new_party = self.sortnstrip(new_party)
        party_details = self.sortnstrip(self.party_data)

        self.assertEqual(party_details, new_party)

    def test_get_all_parties(self):
        self.create_party(self.party_data)
        self.create_party(self.party_data2)

        parties = Party.get_all_parties()
        self.assertEqual(len(parties), 2)

    def test_get_party_id_from_name(self):
        self.create_party(self.party_data)

        name = self.party_data.get('name')
        party_id = Party.get_party_id_from_name(name)
        self.assertEqual(party_id, 1)
