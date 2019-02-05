""""defines implementation to routes for political parties"""
from flask import request
from . import v1_bp
from . import jsonify
from . import utils


@v1_bp.route('/political_party', methods=['POST'])
def political_party():
    """route to create a political party"""
    new_political_party = dict()
    data = request.get_json(force=True)

    try:
        new_political_party['id'] = data['id']
        new_political_party['name'] = data['name']
        new_political_party['hqAddress'] = data['hqAddress']
        new_political_party['logoUrl'] = data['logoUrl']
    except KeyError:
        return jsonify(utils.wrap_response(400, "Please enter a valid request. " +
                                           "Fields include id, name, hqAddress and logoUrl")), 400

    return jsonify(utils.wrap_response(201, new_political_party)), 201
