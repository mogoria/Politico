from . import Base


Offices = []
"""political office model class"""
class PoliticalOffice(Base):
    """Model class for political offices
    stores political offices in list
    """
    def __init__(self):
        super().__init__(Offices)

    def create_office(self, _type, _name):
        """adds office to office list and returns newly created office"""
        if self.get_office_by_name(_name):
            #if office already exists, return empty list
            return {}
        new_office = {
            '_id': self.generate_id(),
            '_type': _type,
            '_name': _name
        }
        Offices.append(new_office)
        return new_office
    @classmethod
    def get_all_offices(cls):
        """returns list of dictionaries of all offices"""
        return Offices

    def get_office_by_id(self, office_id):
        """searches an office by id and returns it"""
        return self.get({"_id":office_id})

    def get_office_by_name(self, office_name):
        """searches an office by name and returns it"""
        return self.get({"_name":office_name})
