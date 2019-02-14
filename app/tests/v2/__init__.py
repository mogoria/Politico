from app.utils.database.init_db import db_con
from app.utils.database.model import Model
import unittest

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.db_con = db_con()
        self.cur = self.db_con.cursor()
    
    def table(self, table_name):
        return Model(table_name)
    
    def tearDown(self):
        if self.db_con:
            self.db_con.close()