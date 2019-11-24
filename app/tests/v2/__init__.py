import unittest
from werkzeug.security import generate_password_hash
from app.utils.database import init_db
from app.utils.database.model import Model
from app.api.v2.models.user_model import User
from app.api.v2.models.office_model import Office
from app.api.v2.models.party_model import Party


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.db_con = init_db.db_con()
        self.cur = self.db_con.cursor()

    def tearDown(self):
        init_db.db_refresh(self.db_con)
        if self.db_con:
            self.db_con.close()


class BaseTestModel(unittest.TestCase):
    def setUp(self):
        init_db.db_refresh()
        if Model.conn_closed():
            Model.open()
        self.password = generate_password_hash("pass123")
        self.user_data = dict(firstname='Tukmen', lastname='Mogoria',
                              othername='Asianut', email='tukmogi@gmail.com',
                              phonenumber='0727296203',
                              passporturi='avatar.com/234',
                              password=self.password, isadmin='True')

        self.user_data2 = dict(firstname='Mary', lastname='Jane',
                               othername='Pink', email='jane@gmail.com',
                               phonenumber='072234366',
                               passporturi='avatar.com/236',
                               password=self.password, isadmin='False')

        self.office_data = dict(name="President", type="state")
        self.office_data2 = dict(name="Governor", type="federal")

        self.party_data = dict(name="Peoples party", logourl="logo.com/23",
                               hqaddress="Nairobi")
        self.party_data2 = dict(name="Jubilee", logourl="logo.com/22",
                                hqaddress="Mombasa")

    @staticmethod
    def sort_dic(dic):
        return {key: dic.get(key) for key in sorted(dic.keys())}

    @staticmethod
    def sortnstrip(dic):
        sorted_dic = BaseTestModel.sort_dic(dic)
        # delete the key id if it exists
        if sorted_dic.get('id'):
            del sorted_dic['id']
        # delete the key isadmin if it exists
        if sorted_dic.get('isadmin'):
            del sorted_dic['isadmin']
        return sorted_dic

    @staticmethod
    def create_user(user_details):
        user = User(** user_details)
        return user.add_user()

    @staticmethod
    def create_party(party_details):
        party = Party(** party_details)
        return party.add_party()

    @staticmethod
    def create_office(office_details):
        office = Office(** office_details)
        return office.add_office()

    def tearDown(self):
        Model.close()
