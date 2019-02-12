""""defines implementation to routes for political parties"""
from flask import request, make_response
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
        null_fields = utils.check_null(new_political_party)
        if not null_fields:
            if PARTY.get_party_by_id(new_political_party['id']):
                #party already exists
                return utils.util_response(409, "Party already exists")
            PARTY.create_party(**new_political_party)
            return make_response(jsonify(utils.wrap_response(201, new_political_party)), 201)
        return utils.util_response(400, "incorrect format. Please provide valid fields for: {}"
                                      .format(", ".join(null_fields)))

    except KeyError:
        return utils.util_response(400, 
                                   "incorrect format. Fields include id, name, hqAddress and logoUrl")

@v1_bp.route('/parties', methods=['GET'])
def get_all_political_parties():
    """route to view all political parties"""
    all_parties = PARTY.get_all_parties()

    if all_parties:
        return utils.util_response(200, all_parties)
    return utils.util_response(404, "parties not found")

@v1_bp.route("/parties/<int:party_id>", methods=['GET'])
def get_specific_political_party(party_id):
    """"route to get specific political party"""
    party = PARTY.get_party_by_id(party_id)
    if party:
        return jsonify(utils.wrap_response(200, PARTY.get_party_by_id(party_id))), 200
    return jsonify(utils.wrap_response(404, "Party not found")), 404

@v1_bp.route("/parties/<int:party_id>/name", methods=["PATCH"])
def edit_specific_political_party(party_id):
    """endpoint to edit specific political party"""
    try:
        data = request.get_json(force=True)
        updated_name = data['name']
        party = PARTY.get_party_by_id(party_id)
        if party:
            party['name'] = updated_name
            PARTY.update_party(**party)
            return jsonify(utils.wrap_response(200, {"message":"party updated successfully"})), 200
        return jsonify(utils.wrap_response(404, "party not found")), 404
    except KeyError:
        return jsonify(utils.wrap_response(400, "incorrect format. " +
                                           "Fields include name")), 400

@v1_bp.route("/parties/<int:party_id>", methods=['DELETE'])
def delete_political_party(party_id):
    """"route to delete specific political party"""
    party_deleted = PARTY.delete_party_by_id(party_id)
    if party_deleted:
        return jsonify(utils.wrap_response(200, {"message":"Party deleted successfully"})), 200
    return jsonify(utils.wrap_response(404, "Party not found")), 404
