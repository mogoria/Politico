class PoliticalOffice:

    def __init__(self):
        self.Offices = []

    def create_office(self, id, type, name):
        new_office = locals()
        del(new_office['self'])
        self.Offices.append(new_office)

    def get_all_offices(self):
        return self.Offices

    def get_office(self, office_id):
        return [office for office in self.Offices if office.get('id')==office_id][0]