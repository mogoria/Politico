"""contains helper functions to routes"""
from flask import make_response
from flask import jsonify
def wrap_response(status_code, data, role):
    """wraps response according to api specification"""
    if 200 <= status_code < 300:
        return {
            "status":status_code,
            role:data if isinstance(data, list) else [data]
        }
    return {
        "status":status_code,
        "error":data
    }

def util_response(status_code, data, role):
    """wraps response in a make_response block"""
    return make_response(
        jsonify(wrap_response(status_code, data, role)), status_code
    )

def check_fields(request, required_fields):
    """decorator to validate required fields"""
    def wrap(func):
        def wrapped_f(*args, **kwargs):
            data = request.get_json()
            message = ""
            if data:
                #get the fields provided int the request
                provided_fields = list(data.keys())
                #check if provided fields match required fields
                if sorted(provided_fields) == sorted(required_fields):
                    return func(*args, **kwargs)

                missing_fields = []
                #get missing required fields
                for field in required_fields:
                    if field not in provided_fields:
                        missing_fields.append(field)

                if missing_fields:
                    message = "Please provide valid fields for: {}"\
                            .format(display_error_fields(missing_fields))
                #the request contains extra fields
                else:
                    message = "Only the following fields are required: {}"\
                            .format(display_error_fields(required_fields))
            else:
                message = "Please enter a valid json request"

            return util_response(400, message, "error")
        # Renaming the function name:
        wrapped_f.__name__ = func.__name__
        return wrapped_f
    return wrap

def display_error_fields(fields):
    """format the display of missing fields"""
    num_fields = len(fields)
    if num_fields == 1:
        return fields[0]
    if num_fields == 2:
        return "{} and {}".format(fields[-2], fields[-1])
    #field length greater than 2
    return "{} and {}".format(",".join(fields[:-1]), fields[-1])

def sanitise(dic):
    """Adds underscores to keys in dictionary"""
    new_dic = dict()
    for key, value in dic.items():
        new_dic["_{}".format(key)] = value
    return new_dic

def desanitise(dic):
    """Removes underscores from dictionary"""
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
        """searches if value is in the office_types list"""
        if office in self.office_types:
            return True
        return False
    @classmethod
    def is_null(cls, value):
        """checks if a value is null"""
        if isinstance(value, str):
            value = value.strip()
        return value == ""

    def is_url(self, value):
        """checks wheter a url is valid"""
        is_url = '.' in value
        return is_url

    def is_str(self, value):
        """Returns True if value isn't a number and contains letters and spaces but not null"""
        #confirm that value is not null and not an integer
        if self.is_int(value) or self.is_null(value):
            return False
        for char in value:
            #only accept spaces and alphabets
            if not (char.isalpha() or char == " "):
                return False
        return True

    def is_int(self, value):
        """Returns true if a value is an integer"""
        try:
            int(value)
        except ValueError:
            return False
        return True

    def mass_non_null(self, null_list):
        """Checks a dictionary to make sure that the values are not null"""
        for key, value in null_list.items():
            if self.is_null(value):
                self.errors.append("Please enter a value for {}".format(key))
        return self.errors

    def mass_check_type(self, type_list, values):
        """Checks a dictionary of values to see whether they are of the type provided in typelist"""
        for key, value in type_list.items():
            if not value(values.get(key)):
                self.errors.append("Please enter a valid {}".format(key))
        return self.errors

class OfficeValidator(Validator):
    """validates office input"""
    def __init__(self, type, name):
        super().__init__()
        self.type = type
        self.name = name

    def validate(self):
        """Returns an error if validation fails found otherwise empty list"""
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
        if self.mass_check_type(type_list, values):
            return self.errors
        if not self.check_office_type(self.type):
            return "Please enter a valid type either: {}".format(", ".join(self.office_types))
        return []



class PartyValidator(Validator):
    """Validates party fields"""
    def __init__(self, name, hqAddress, logoUrl):
        super().__init__()
        self.name = name
        self.hqAddress = hqAddress
        self.logoUrl = logoUrl

    def validate(self):
        """Returns an error if validation fails found otherwise empty list"""
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

        if self.mass_non_null(values):
            return self.errors
        if self.mass_check_type(type_list, values):
            return self.errors
        return []
