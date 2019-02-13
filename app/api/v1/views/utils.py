"""contains helper functions to routes"""
from flask import make_response
from flask import jsonify
def wrap_response(status_code, data):
    """wraps response according to api specification"""
    if 200 <= status_code < 300:
        return {
            "status":status_code,
            "data":data if isinstance(data, list) else [data]
        }
    return {
        "status":status_code,
        "error":data
    }

def util_response(status_code, data):
    """wraps response in a make_response block"""
    return make_response(
        jsonify(wrap_response(status_code, data)), status_code
    )

def check_valid_fields(data, valid_fields):
    """returns False if data:
    - Doesn't have all keys in field list
    - Contains keys not in valid field list"""
    for field in valid_fields:
        if not data.get(field):
            return False
    
    if len(valid_fields) != len(data.keys()):
        return False
    return True

def check_valid_type(data, sample_data):
    """checks if data has same type of values in sample data
    returns a list of faulty types """
    response = []

    for key, value in data.items():
        if not isinstance(value, type(sample_data.get(key))):
            response.append(key)

    return response

def check_null(data):
    null_fields = []
    for field, value in data.items():
        if not value:
            null_fields.append(field)
    return null_fields

def sanitise(dic):
    new_dic = dict()
    for key, value in dic.items():
        new_dic["_{}".format(key)] = value
    return new_dic

def desanitise(dic):
    new_dic = dict()
    for key, value in dic.items():
        #omit the underscore from the key name
        new_dic[key[1:]] = value
    return new_dic

class Validator:
    office_types = ["federal", "legislative", "state", "local government"]

    def __init__(self):
        self.errors = []

    def check_office_type(self, office):
        if office in self.office_types:
            return True
        return False

    def is_null(self, value):
        if isinstance(value, str):
            value = value.strip()
        return value == ""

    def is_url(self, value):
        if "." in value:
            return True 
        else:
            return False

    def is_str(self, value):
        if isinstance(value, str):
            return value.isalpha()
        return False

    def is_int(self, value):
        try:
            int(value)
        except ValueError:
            return False
        return True

    def mass_non_null(self, null_list):
        for key, value in null_list.items():
                if self.is_null(value):
                    self.errors.append("Please enter a value for {}".format(key))
        return self.errors

    def mass_check_type(self, type_list, values):
        for k, v in type_list.items():
            if not v(values.get(k)):
                self.errors.append("Please enter a valid {}".format(k))
        return self.errors

class OfficeValidator(Validator):
    def __init__(self, type, name):
        super().__init__()
        self.type = type
        self.name = name

    def validate(self):
        values = {
            "type": self.type,
            "name": self.name
        }
        type_list = {
            "type": self.is_str,
            "name": self.is_str
        }
        if self.mass_non_null(values):
            return self.errors
        elif self.mass_check_type(type_list, values):
            return self.errors
        elif not self.check_office_type(type):
            return "Please enter a valid type {}".format(",".join(self.office_types))
        return []



class PartyValidator(Validator):
    def __init__(self, name, hqAddress, logoUrl):
        super().__init__()
        self.name = name
        self.hqAddress = hqAddress
        self.logoUrl = logoUrl

    def validate(self):
        values = {
            "name": self.name,
            "hqAddress": self.hqAddress,
            "logoUrl": self.logoUrl
        }
        type_list = {
            "name": self.is_str,
            "hqAddress": self.is_str,
            "logoUrl": self.is_url
        }

        if(self.mass_non_null(values)):
            return self.errors
        elif (self.mass_check_type(type_list, values)):
            return self.errors
        return []
        