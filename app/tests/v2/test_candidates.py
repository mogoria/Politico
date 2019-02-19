from app.api.v2.models.office_model import Office
from app.api.v2.models.party_model import Party
from app.api.v2.models.user_model import User
from app.api.v2.models.candidate_model import Candidate
from . import BaseTestModel


class TestCandidateModel(BaseTestModel):
    candidate_data = dict(email='tukmogi@gmail.com', party_name='independent',
                          office_name='president')

    @staticmethod
    def decode_candidate_data(candidate_data):
        email = candidate_data.get('email')
        party_name = candidate_data.get('party_name')
        office_name = candidate_data.get('office_name')

        user_id = User.get_user_id_from_email(email)
        party_id = Party.get_party_id_from_name(party_name)
        office_id = Office.get_office_id_from_name(office_name)

        return dict(candidate=user_id, party=party_id, office=office_id)

    def create_candidate(self, user_data, party_data, office_data):
        #create a user
        self.create_user(user_data)
        #create a party
        self.create_party(party_data)
        #create an office
        self.create_office(office_data)

        candidate_data = dict(email=user_data.get('email'), party_name=party_data.get('name'),
                              office_name=office_data.get('name'))

        candidate_data = self.decode_candidate_data(candidate_data)
        candidate = Candidate(** candidate_data)
        return candidate.add_candidate()
    
    def test_add_candidate(self):
        
        new_candidate = self.create_candidate(self.user_data, self.party_data, self.office_data)
        

        user_id = User.get_user_id_from_email(self.user_data.get('email'))
        party_id = Party.get_party_id_from_name(self.party_data.get('name'))
        office_id = Office.get_office_id_from_name(self.office_data.get('name'))
        cand = dict(candidate=user_id, party=party_id, office=office_id)
        
        self.assertEqual(new_candidate, cand)

    def test_get_all_candidates(self):
        #create two candidates
        self.create_candidate(self.user_data, self.party_data, self.office_data)
        self.create_candidate(self.user_data2, self.party_data2, self.office_data2)

        candidates = Candidate.get_all_candidates()
        self.assertEqual(len(candidates), 2)

    def test_get_candidate_by_email(self):
        new_cand = self.create_candidate(self.user_data, self.party_data, self.office_data)

        reteived_candidate = Candidate.get_candidate_by_email(self.user_data.get('email'))
        self.assertEqual(reteived_candidate, new_cand)
