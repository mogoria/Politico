from werkzeug.security import generate_password_hash
from . import BaseTest


class TestDB(BaseTest):
    def test_connection(self):
        cur = self.db_con.cursor()
        cur.execute("SELECT VERSION()")
        res = cur.fetchone()
        self.assertIn("PostgreSQL", res[0])

    def test_create_user(self):
        password = generate_password_hash('not-sure')
        email = 'test@localhost.com'
        insert_query = """
        INSERT INTO users(firstname, lastname, phoneNumber, email, password, isAdmin)
            VALUES('Mary', 'Jane', 0700222333, '{}', '{}', True)
        """.format(email, password)
        self.cur.execute(insert_query)
        self.db_con.commit()

        select_query = """
        SELECT email FROM USERS WHERE email = '{}'
        """.format(email)
        cur =  self.db_con.cursor()
        cur.execute(select_query)
        res = cur.fetchone()
        self.assertEqual(email, res[0])