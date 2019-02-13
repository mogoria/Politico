from . import unittest
from app.api.v1.views.utils import Validator, PartyValidator, OfficeValidator

class TestValidator(unittest.TestCase):
    def setUp(self):
        self.valid_party = {
            "name": "my party",
            "logoUrl": "photo.com",
            "hqAddress": "Nairobi"
        }
        

class TestPartyValidator(TestValidator):
    def test_valid_party(self):
        validator = PartyValidator(** self.valid_party)
        self.assertTrue(validator.validate(), [])

    def test_blank_name(self):
        values = self.valid_party
        values['name'] = ''
        print(values)
        validator = PartyValidator(** values)
        self.assertIn("Please enter a value for name", validator.validate())

    def test_invalid_name(self):
        values = self.valid_party
        values['name'] = 12
        print(values)
        validator = PartyValidator(** values)
        self.assertIn("Please enter a valid name", validator.validate())