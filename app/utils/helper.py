from flask import jsonify, make_response


def handle_bad_request(e):
    return make_response(jsonify({
        "status": 400,
        "error": "Bad request"
    }), 400)


def handle_not_found(e):
    return make_response(jsonify({
        "status": 404,
        "error": "Not found"
    }), 404)


def wrap_response(status_code, data, role):
    """wraps response according to api specification"""
    if 200 <= status_code < 300:
        return {
            "status": status_code,
            role: data if isinstance(data, list) else [data]
        }
    return {
        "status": status_code,
        "error": data
    }


def format_field_display(fields):
    """format the display of missing fields"""
    if len(fields) == 1:
        return fields[0]
    return "{} and {}".format(", ".join(fields[:-1]), fields[-1])   


def util_response(status_code, data, role):
    """wraps response in a make_response block"""
    return make_response(
        jsonify(wrap_response(status_code, data, role)), status_code
    )
