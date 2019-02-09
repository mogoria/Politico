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
    print("Null fields: {}".format(null_fields))
    return null_fields
