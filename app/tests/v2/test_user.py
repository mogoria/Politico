#postgres://postgres:1A2S3D@localhost:5432/andela_test
from . import BaseTestModel
from app.api.v2.models.user_model import User


class TestUserModel(BaseTestModel):
    def setUp(self):
        super().setUp()

    def test_insert_to_db(self):
        user = User(** self.user_data)
        new_user = user.add_user()

        self.assertEqual(new_user, self.user_data)

    def test_get_user_by_email(self):
        user = User(** self.user_data)
        user.add_user()

        email = self.user_data.get('email')
        added_user = User.get_user_by_email(email)
        added_user = self.sortnstrip(added_user)
        user_data = self.sortnstrip(self.user_data)

        self.assertEqual(added_user, user_data)

    def test_get_all_users(self):
        user1 = User(** self.user_data)
        user2 = User(** self.user_data2)
        user1.add_user()
        user2.add_user()

        users = User.get_all_users()
        self.assertEqual(len(users), 2)

    def test_get_user_id_from_email(self):
        user = User(** self.user_data)
        user.add_user()

        email = self.user_data.get('email')
        user_id = User.get_user_id_from_email(email)
        self.assertEqual(user_id, 1)
