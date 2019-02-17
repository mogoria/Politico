from app.utils.database.model import Model
class Office(Model):
    table_name = "offices"
    columns = ('name', 'type')

    def __init__(self, name, type):
        super().__init__()

        self.name = name
        self.type = type

    @classmethod
    def get_all_offices(cls):
        offices = cls.select_all(table_name=cls.table_name, columns=cls.columns)
        return offices

    @classmethod
    def get_office_by_name(cls, name):
        office = cls.select_one(table_name=cls.table_name, criteria="name='{}'".format(name))
        return office

    @classmethod
    def get_office_id_from_name(cls, name):
        office_id = cls.select_one(table_name=cls.table_name, columns=['id'], criteria="name='{}'".format(name))
        return office_id.get('id')

    def add_office(self):
        office_details = [self.name, self.type]
        self.insert(self.table_name, self.columns, office_details)
        return dict(zip(self.columns, office_details))
