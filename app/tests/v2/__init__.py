import unittest
from werkzeug.security import generate_password_hash
from app.utils.database import init_db


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
        self.password = generate_password_hash("pass123")
        self.dummy_data = dict(firstname='Tukmen', lastname='Mogoria',
                               othername='Asianut', email='tukmogi@gmail.com',
                               phonenumber='0727296203', passporturi='avatar.com/234',
                               password=self.password, isadmin='True')

        self.dummy_data2 = dict(firstname='Mary', lastname='Jane',
                                othername='Pink', email='jane@gmail.com',
                                phonenumber='072234366', passporturi='avatar.com/236',
                                password=self.password, isadmin='False')

    @staticmethod
    def sort_dic(dic):
        return {key:dic.get(key) for key in sorted(dic.keys())}

    @staticmethod
    def sortnstrip(dic):
        sorted_dic = BaseTestModel.sort_dic(dic)
        #delete the key id if it exists
        if sorted_dic.get('id'):
            del sorted_dic['id']
        #delete the key isadmin if it exists
        if sorted_dic.get('isadmin'):
            del sorted_dic['isadmin']
        return sorted_dic