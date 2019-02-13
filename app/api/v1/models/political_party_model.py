Parties = []
class PoliticalParty():
    """A class used to store and retrieve political parties"""

    def create_party(self, _name, _hqAddress, _logoUrl):
        """Save new party to parties dictionary"""
        new_party = dict()
        #check if party exists
        if not self.get_party_by_name(_name):            
            new_party = {
                "_id": self.generate_id(),
                "_name": _name,
                "_hqAddress": _hqAddress,
                "_logoUrl": _logoUrl
            }
            Parties.append(new_party)
        return new_party

    def update_party(self, _id, _name, _hqAddress=None, _logoUrl=None):
        """Updates a party by searching the id provided"""
        if Parties:
            for party in Parties:
                if party.get('_id') == _id:
                    party['_name'] = _name
                    return {
                        "id": party.get('_id'),
                        "name": _name
                    }
        return {}


    def get_all_parties(self):
        """returns a list of party objects"""
        return Parties

    def get_party_by_id(self, _id):
        """returns dictionary if present and empty dictionary if absent"""
        found_party = [party for party in Parties if party.get('_id') == _id]
        if found_party:
            return found_party[0]
        return {}

    def get_party_by_name(self, name):
        """returns office if present and empty if absent"""
        found_party = [party for party in Parties if party.get('_name') == name]
        if found_party:
            return found_party[0]
        return {}

    def delete_party_by_id(self, _id):
        """returns True if successful and False if unsuccessful"""
        if self.get_party_by_id(_id):
            for party in Parties:
                if party.get('_id') == _id:
                    Parties.remove(party)
                    return True
        return False
    def generate_id(self):
        if not Parties:
            return 1
        return Parties[-1].get('_id') + 1