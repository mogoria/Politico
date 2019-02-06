""""defines implementation to routes for political parties"""
from flask import request
from app.api.v1.models.political_party_model import PoliticalParty
from . import v1_bp
from . import jsonify
from . import utils

PARTY = PoliticalParty()

@v1_bp.route('/parties', methods=['POST'])
def post_political_party():
    """route to create a political party"""
    new_political_party = dict()
    data = request.get_json(force=True)

    try:
        new_political_party = {
            'id' : data['id'],
            'name' : data['name'],
            'hqAddress' : data['hqAddress'],
            'logoUrl' : data['logoUrl']
            }

        if PARTY.get_party_by_id(new_political_party['id']):
            #party already exists
            return jsonify(utils.wrap_response(409, "Party already exists"))
        PARTY.create_party(**new_political_party)
        return jsonify(utils.wrap_response(201, new_political_party)), 201

    except KeyError:
        return jsonify(utils.wrap_response(400, "Please enter a valid request. " +
                                           "Fields include id, name, hqAddress and logoUrl")), 400

@v1_bp.route('/parties', methods=['GET'])
def get_all_political_parties():
    """route to view all political parties"""
    all_parties = PARTY.get_all_parties()

    if all_parties:
        return jsonify(utils.wrap_response(200, all_parties)), 200
    return jsonify(utils.wrap_response(404, "No data available")), 404

@v1_bp.route("/parties/<int:party_id>", methods=['GET'])
def get_specific_political_party(party_id):
    """"route to get specific political party"""
    party = PARTY.get_party_by_id(party_id)
    if party:
        return jsonify(utils.wrap_response(200, PARTY.get_party_by_id(party_id))), 200 
    return jsonify(utils.wrap_response(404, "Party not found")), 404
