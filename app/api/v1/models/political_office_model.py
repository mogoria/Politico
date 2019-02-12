Offices = []
"""political office model class"""
class PoliticalOffice:
    """Model class for political offices
    stores political offices in list
    """

    def create_office(self, _id, _type, _name):
        """adds office to office list and returns newly created office"""
        
        if self.get_office_by_id(_id) or self.get_office_by_name(_name):
            #if office already exists, return empty list
            return {}
        else:
            new_office = {
                '_id':_id,
                '_type': _type,
                '_name': _name
            }
            Offices.append(new_office)
            return new_office

    def get_all_offices(self):
        """returns list of dictionaries of all offices"""
        return Offices

    def get_office_by_id(self, office_id):
        """searches an office by id and returns it"""
        found_office = [office for office in Offices if office.get('_id') == office_id]
        if found_office:
            return found_office[0]
        return {}

    def get_office_by_name(self, office_name):
        """searches an office by name and returns it"""
        office = [office for office in Offices if office.get("_name") == office_name]
        if office:
            return office[0]
        return {}