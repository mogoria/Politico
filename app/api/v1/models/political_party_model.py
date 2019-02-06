class PoliticalParty():
    """A class used to store and retrieve political parties"""
    def __init__(self):
        self.parties = {}

    def create_party(self, id, name, hqAddress, logoUrl):
        """Save new party to parties dictionary"""
        new_party = dict()
        new_party['id'] = id
        new_party['name'] = name
        new_party['hqAddress'] = hqAddress
        new_party['logoUrl'] = logoUrl

        self.parties[id] = new_party
        return new_party

    def update_party(self, id, name, hqAddress, logoUrl):
        """Updates a party by searching the id provided"""
        if self.parties:
            if id in self.parties:
                self.parties[id]['id'] = id
                self.parties[id]['name'] = name
                self.parties[id]['hqAddress'] = hqAddress
                self.parties[id]['logoUrl'] = logoUrl
                return self.parties[id]
        return {}


    def get_all_parties(self):
        """returns a list of party objects"""
        return list(self.parties.values())

    def get_party_by_id(self, id):
        """returns dictionary if present and empty dictionary if absent"""
        return self.parties.get(id, {})

    def delete_party_by_id(self, id):
        """returns True if successful and False if unsuccessful"""
        try:
            return bool(self.parties.pop(id) != id)
        except KeyError:
            return False
