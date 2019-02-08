from app.api.v1.models.political_office_model import PoliticalOffice
import unittest
from . import BaseTest



class TestOfficeModel(unittest.TestCase):
    def setUp(self):
        self.offices = PoliticalOffice()
        self.office1 = {
            "office_id":76,
            "office_type":"type1",
            "office_name":"office1"
        }
    def test_create_office(self):
        pass

    def test_get_all_offices(self):
        pass

    def test_get_single_office(self):
        pass