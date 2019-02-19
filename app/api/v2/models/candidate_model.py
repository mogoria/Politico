from app.utils.database.model import Model


class Candidate(Model):
    table_name = 'candidates'

    def __init__(self, user, party, office):
        super().__init__()
        pass

    def add_candidate(self):
        pass

    @classmethod
    def get_all_candidates(cls):
        pass

    @classmethod
    def get_candidate_by_email(cls, email):
        pass
