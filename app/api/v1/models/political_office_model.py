"""political office model class"""
class PoliticalOffice:
    """Model class for political offices
    stores political offices in list
    """

    def __init__(self):
        self.Offices = []

    def create_office(self, id, type, name):
        """adds office to office list and returns newly created office"""
        
        if self.get_office_by_id(id) or self.get_office_by_name(name):
            #if office already exists, return empty list
            return {}
        new_office = {
            'id':id,
            'type': type,
            'name': name
        }
        self.Offices.append(new_office)
        return new_office

    def get_all_offices(self):
        """returns list of dictionaries of all offices"""
        return self.Offices

    def get_office_by_id(self, office_id):
        """searches an office by id and returns it"""
        found_office = [office for office in self.Offices if office.get('id') == office_id]
        if found_office:
            return found_office[0]
        return {}

    def get_office_by_name(self, office_name):
        """searches an office by name and returns it"""
        office = [office for office in self.Offices if office.get("name") == office_name]
        if office:
            return office[0]
        return {}