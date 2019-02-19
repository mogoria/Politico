from app.api.v1.views.utils import Validator, PartyValidator, OfficeValidator
from . import unittest


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.valid_party = {
            "name": "my party",
            "logoUrl": "photo.com",
            "hqAddress": "Nairobi"
        }

        self.valid_office = {
            "type": "legislative",
            "name": "office"
        }


class TestPartyValidator(TestValidator):
    def test_valid_party(self):
        validator = PartyValidator(** self.valid_party)
        self.assertEqual(validator.validate(), [])

    def test_blank_name(self):
        values = self.valid_party
        values['name'] = ''
        validator = PartyValidator(** values)
        self.assertIn("Please enter a value for name", validator.validate())

    def test_invalid_name(self):
        values = self.valid_party
        values['name'] = 12
        validator = PartyValidator(** values)
        self.assertIn("Please enter a valid name", validator.validate())

class TestOfficeValidator(TestValidator):
    def test_valid_party(self):
        validator = OfficeValidator(**self.valid_office)
        self.assertEqual(validator.validate(), [])

    def test_invalid_type(self):
        office = self.valid_office
        office['type'] = 'weird type'
        validator = OfficeValidator(**office)
        self.assertIn('enter a valid type', validator.validate())
