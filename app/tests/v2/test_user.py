#postgres://postgres:1A2S3D@localhost:5432/andela_test
from unittest import TestCase
from werkzeug.security import generate_password_hash
from app.api.v2.models.user_model import User
from app.utils.database import init_db


class TestUserModel(TestCase):
    def setUp(self):
        password = generate_password_hash('pass123')
        self.dummy_data = dict(firstname='Tukmen', lastname='Mogoria',
                               othername='Asianut', email='tukmogi@gmail.com',
                               phonenumber='0727296203', passporturi='avatar.com/234',
                               password=password, isadmin='True')

        self.dummy_data2 = dict(firstname='Mary', lastname='Jane',
                                othername='Pink', email='jane@gmail.com',
                                phonenumber='072234366', passporturi='avatar.com/236',
                                password=password, isadmin='False')

    def sort_dic(self, dic):
        return {key:dic.get(key) for key in sorted(dic.keys())}

    def sortnstrip(self, dic):
        sorted_dic = self.sort_dic(dic)
        #delete the key id if it exists
        if sorted_dic.get('id'):
            del sorted_dic['id']
        #delete the key isadmin if it exists
        if sorted_dic.get('isadmin'):
            del sorted_dic['isadmin']
        return sorted_dic

    def test_insert_to_db(self):
        user = User(** self.dummy_data)
        new_user = user.add_user()

        self.assertEqual(new_user, self.dummy_data)

    def test_get_user_by_email(self):
        user = User(** self.dummy_data)
        user.add_user()

        email = self.dummy_data.get('email')
        added_user = User.get_user_by_email(email)
        added_user = self.sortnstrip(added_user)
        dummy_data = self.sortnstrip(self.dummy_data)

        self.assertEqual(added_user, dummy_data)

    def test_get_all_users(self):
        user1 = User(** self.dummy_data)
        user2 = User(** self.dummy_data2)
        user1.add_user()
        user2.add_user()

        users = User.get_all_users()
        self.assertEqual(len(users), 2)

    def test_get_user_id_from_email(self):
        user = User(** self.dummy_data)
        user.add_user()

        email = self.dummy_data.get('email')
        user_id = User.get_user_id_from_email(email)
        self.assertEqual(user_id, 1)

    def tearDown(self):
        User.close()
        init_db.db_refresh()
