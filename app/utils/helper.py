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
