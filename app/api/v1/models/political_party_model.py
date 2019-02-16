from . import Base


Parties = []
class PoliticalParty(Base):
    """A class used to store and retrieve political parties"""
    def __init__(self):
        super().__init__(Parties)

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
    @classmethod
    def update_party(cls, _id, _name, _hqAddress=None, _logoUrl=None):
        """Updates a party by searching the id provided"""

        edittable = dict(_id=_id, _name=_name, _hqAddress=_hqAddress, _logoUrl=_logoUrl)
        editted_fields = {}

        for party in Parties:
            if party.get('_id') == _id:
                for key, value in edittable.items():
                    #check if value is not null and doesn't match existing value
                    if key == '_id' or (value and party[key] != value):
                        party[key] = value
                        editted_fields[key] = value

        #check if data has been changed
        if len(editted_fields.keys()) < 2:
            #no change
            return {"message": "nothing to change"}

        return editted_fields

    @classmethod
    def get_all_parties(cls):
        """returns a list of party objects"""
        return Parties

    def get_party_by_id(self, _id):
        """returns dictionary if present and empty dictionary if absent"""
        return self.get({"_id":_id})

    def get_party_by_name(self, name):
        """returns office if present and empty if absent"""
        return self.get({"_name":name})

    @classmethod
    def delete_party_by_id(cls, _id):
        """returns True if successful and False if unsuccessful"""
        for party in Parties:
            #remove party if it exists in the party list
            if party.get('_id') == _id:
                Parties.remove(party)
                return True
        return False
