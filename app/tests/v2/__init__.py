from app.utils.database import db_con
import unittest

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.db_con = db_con()
    
    def tearDown(self):
        if self.db_con:
            self.db_con.close()