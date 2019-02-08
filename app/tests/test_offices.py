from app.api.v1.models.political_office_model import PoliticalOffice
import unittest
from . import BaseTest

class InitOffice:
    Office = PoliticalOffice()
    office1 = {
        "id":76,
        "type":"type1",
        "name":"office1"
    }
    office2 = {
        "id":22,
        "type":"type2",
        "name":"office2"
    }

class BaseOfficeClass(InitOffice, BaseTest):
    path = "/api/v1/offices"


class TestOfficeModel(InitOffice, unittest.TestCase):         
    def test_create_office(self):
        self.Office.create_office(** self.office1)
        self.assertEqual(len(self.Office.Offices), 1)
        self.assertEqual(self.Office.Offices[0], self.office1)

    def test_get_all_offices(self):
        self.Office.Offices.clear()
        self.Office.create_office(** self.office1)
        self.Office.create_office(** self.office2)
        self.assertEqual(len(self.Office.get_all_offices()), 2)

    def test_get_single_office(self):
        res = self.Office.get_office(22)
        self.assertEqual(res, self.office2)

class TestOfficeStatusCodes(BaseOfficeClass):
    def test_create_office(self):
        resp = self.post(self.office1)
        self.assertEqual(resp.status_code, 201)
