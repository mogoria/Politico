from . import BaseTest


class TestDB(BaseTest):
    def test_connection(self):
        cur = self.db_con.cursor()
        cur.execute("SELECT VERSION()")
        res = cur.fetchone()
        print(res)
        self.assertIn("PostgreSQL 10.6", res[0])