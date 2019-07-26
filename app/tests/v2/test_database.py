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
        INSERT INTO users(firstname, lastname, phoneNumber,
                          email, password, isAdmin)
            VALUES(%s, %s, %s, %s, %s, %s);
        """
        values = ('Mary', 'Jane', '0700222333', email, password, True)
        self.cur.execute(insert_query, values)
        self.db_con.commit()

        select_query = "SELECT email FROM USERS WHERE email = %s"
        cur = self.db_con.cursor()
        cur.execute(select_query, (email,))
        res = cur.fetchone()
        self.assertEqual(email, res[0])
