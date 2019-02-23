from app.utils.database.model import Model


class User(Model):
    table_name = "users"
    columns = ('firstname', 'lastname', 'othername', 'email',
               'phonenumber', 'passporturi', 'password', 'isadmin')

    def __init__(self, **kwargs):
        super().__init__()

        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.othername = kwargs.get('othername')
        self.email = kwargs.get('email')
        self.phonenumber = kwargs.get('phonenumber')
        self.passporturi = kwargs.get('passporturi')
        self.password = kwargs.get('password')
        self.isadmin = kwargs.get('isadmin')

    @classmethod
    def get_all_users(cls):
        users = cls.select_all(table_name=cls.table_name, columns=cls.columns)
        return users

    @classmethod
    def get_user_by_email(cls, email):
        user = cls.select_one(table_name=cls.table_name,
                              criteria="email='{}'".format(email))
        return user

    @classmethod
    def get_user_id_from_email(cls, email):
        user_id = cls.select_one(table_name=cls.table_name, columns=['id'],
                                 criteria="email='{}'".format(email))
        return user_id.get('id')

    def add_user(self):
        user_details = [self.firstname, self.lastname, self.othername,
                        self.email, self.phonenumber, self.passporturi,
                        self.password, self.isadmin]
        self.insert(self.table_name, self.columns, user_details)
        return dict(zip(self.columns, user_details))
