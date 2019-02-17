from app.api.v2.models.office_model import Office
from app.utils.database import init_db
from . import BaseTestModel


class TestOfficeModel(BaseTestModel):
    def setUp(self):
        super().setUp()
        self.data1 = dict(name="President", type="state")
        self.data2 = dict(name="Governor", type="federal")
        self.invalid_data = dict(name="Governor", type="unregistered")

    def test_create_office(self):
        office = Office(** self.data1)
        new_office = office.add_office()
        self.assertEqual(new_office, self.data1)

    def test_get_office_by_name(self):
        office = Office(** self.data1)
        office.add_office()

        name = self.data1.get('name')
        new_office = Office.get_office_by_name(name)

        new_office = self.sortnstrip(new_office)
        office_details = self.sortnstrip(self.data1)
    
        self.assertEqual(office_details, new_office)

    def test_get_all_offices(self):
        office1 = Office(** self.data1)
        office2 = Office(** self.data2)
        office1.add_office()
        office2.add_office()

        offices = Office.get_all_offices()
        self.assertTrue(len(offices), 2)

    def test_get_office_id_from_name(self):
        office = Office(** self.data1)
        office.add_office()
        
        office_id = Office.get_office_id_from_name(self.data1.get('name'))
        self.assertEqual(office_id, 1)

    def tearDown(self):
        Office.close()
        init_db.db_refresh()