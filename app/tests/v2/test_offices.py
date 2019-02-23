from app.api.v2.models.office_model import Office
from . import BaseTestModel


class TestOfficeModel(BaseTestModel):
    def setUp(self):
        super().setUp()
        self.invalid_data = dict(name="Governor", type="unregistered")

    def test_create_office(self):
        office = Office(** self.office_data)
        new_office = office.add_office()
        self.assertEqual(new_office, self.office_data)

    def test_get_office_by_name(self):
        office = Office(** self.office_data)
        office.add_office()

        name = self.office_data.get('name')
        new_office = Office.get_office_by_name(name)

        new_office = self.sortnstrip(new_office)
        office_details = self.sortnstrip(self.office_data)

        self.assertEqual(office_details, new_office)

    def test_get_all_offices(self):
        office1 = Office(** self.office_data)
        office2 = Office(** self.office_data2)
        office1.add_office()
        office2.add_office()

        offices = Office.get_all_offices()
        self.assertEqual(len(offices), 2)

    def test_get_office_id_from_name(self):
        office = Office(** self.office_data)
        office.add_office()

        off_id = Office.get_office_id_from_name(self.office_data.get('name'))
        self.assertEqual(off_id, 1)
