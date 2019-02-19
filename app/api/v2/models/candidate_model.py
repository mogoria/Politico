from app.utils.database.model import Model
from .user_model import User


class Candidate(Model):
    table_name = 'candidates'
    columns = ('candidate',#user id
               'party',#party id
               'office')#office id

    def __init__(self, candidate, party, office):
        super().__init__()
        self.candidate = candidate
        self.party = party
        self.office = office

    def add_candidate(self):
        candidate = [self.candidate, self.party, self.office]
        self.insert(self.table_name, self.columns, candidate)
        return dict(zip(self.columns, candidate))

    @classmethod
    def get_all_candidates(cls):
        candidates = cls.select_all(table_name=cls.table_name, columns=cls.columns)
        return candidates

    @classmethod
    def get_candidate_by_email(cls, email):
        """returns a candidate given the email
        
        Arguments:
            email {Str} -- email of the candidate
        """
        cand_id = User.get_user_by_email(email)
        return cls.get_candidate_by_id(cand_id.get('id'))

    @classmethod
    def get_candidate_by_id(cls, cand_id):
        cand = cls.select_one(table_name=cls.table_name, columns=cls.columns,
                              criteria='candidate={}'.format(cand_id))
        return cand
