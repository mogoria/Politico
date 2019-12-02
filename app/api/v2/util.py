import re
from flask import jsonify, make_response
from app.utils.helper import wrap_response, format_field_display

USER_FIELDS = ('firstname', 'lastname', 'othername', 'email',
               'phonenumber', 'passporturi', 'password', 'isadmin')


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
                # get the fields provided in the request
                provided_fields = list(data.keys())

                # check if provided fields match required fields
                if sorted(provided_fields) == sorted(required_fields):
                    return func(*args, **kwargs)

                # get missing required fields
                missing_fields = [
                    field for field in required_fields if field not in provided_fields]

                # get extra fields
                black_sheep = [
                    field for field in provided_fields if field not in required_fields]

                if missing_fields:
                    message = "Please provide valid fields for: {}"\
                        .format(format_field_display(missing_fields))
                # the request contains extra fields
                elif black_sheep:
                    message = "The following fields are invalid: {}"\
                        .format(format_field_display(black_sheep))
            else:
                message = "Please enter a valid json request"

            return util_response(400, message, "error")
        # Renaming the function name:
        wrapped_f.__name__ = func.__name__
        return wrapped_f
    return wrap


class validate_user:
    errors = []
    user = dict()

    def __init__(self, **kw):
        self.user = {field: kw.get(field) for field in USER_FIELDS}

    def validate(self):
        non_null = ['firstname', 'email', 'phonenumber', 'password']
        null_fields = []
        message = ''

        for field in non_null:
            if self.user.get(field) is '':
                null_fields.append(field)

        if null_fields:
            message = "Required values: " + format_field_display(null_fields)
        elif not valid_email(self.user.get('email')):
            message = "Please enter a valid email"
        elif not valid_phone(self.user.get("phonenumber")):
            message = "Please enter a valid phone number"
        elif not valid_password(self.user.get("password")):
            message = "Please enter a valid password"
        return message


def valid_email(email):
    # This sure doesn't meet standard but works for now
    return re.match(r'^\S+@\S+\.\S+$', email)


def valid_phone(phone):
    return re.match(r'(0|\+254)7[0-9]{8}', phone)


def valid_password(password):
    return len(password) >= 8
