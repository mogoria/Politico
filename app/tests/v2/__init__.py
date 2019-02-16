from app.utils.database import init_db
from app.utils.database.model import Model
import unittest

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.db_con = init_db.db_con()
        self.cur = self.db_con.cursor()
    
    def table(self, table_name):
        return Model(table_name)
    
    def tearDown(self):
        init_db.db_refresh(self.db_con)
        if self.db_con:
            self.db_con.close()