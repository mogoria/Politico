#postgres://postgres:1A2S3D@localhost:5432/andela_test
from . import BaseTestModel
from app.api.v2.models.user_model import User
from app.utils.database import init_db


class TestUserModel(BaseTestModel):
    def setUp(self):
        super().setUp()

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
