from app.utils.database.model import Model


class Party(Model):
    table_name = "parties"
    columns = ('name', 'logourl', 'hqaddress')

    def __init__(self, name, logourl, hqaddress):
        super().__init__()
        self.name = name
        self.logourl = logourl
        self.hqaddress = hqaddress

    @classmethod
    def get_all_parties(cls):
        parties = cls.select_all(table_name=cls.table_name,
                                 columns=cls.columns)
        return parties

    @classmethod
    def get_party_by_name(cls, name):
        party = cls.select_one(table_name=cls.table_name,
                               criteria={'column': 'name', 'value': name})
        return party

    @classmethod
    def get_party_id_from_name(cls, name):
        party_id = cls.select_one(table_name=cls.table_name, columns=['id'],
                                  criteria={'column': 'name', 'value': name})
        return party_id.get('id')

    def add_party(self):
        party_details = [self.name, self.logourl, self.hqaddress]
        self.insert(self.table_name, self.columns, party_details)
        return dict(zip(self.columns, party_details))
