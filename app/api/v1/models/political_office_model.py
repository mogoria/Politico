"""political office model class"""
class PoliticalOffice:
    """Model class for political offices
    stores political offices in list
    """

    def __init__(self):
        self.Offices = []

    def create_office(self, id, type, name):
        """adds office to office list and returns newly created office"""
        new_office = locals()
        del new_office['self']
        self.Offices.append(new_office)
        return new_office

    def get_all_offices(self):
        """returns list of dictionaries of all offices"""
        return self.Offices

    def get_office(self, office_id):
        """searches an office by id and returns it"""
        return [office for office in self.Offices if office.get('id') == office_id][0]
