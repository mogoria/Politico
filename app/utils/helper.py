from flask import jsonify, make_response
def handle_bad_request(e):
    return make_response(jsonify({
        "status": 400,
        "error": "Bad request"
    }))