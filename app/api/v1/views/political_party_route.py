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
    role = "party"
    new_political_party = dict()
    data = request.get_json(force=True)

    try:
        new_political_party = {
            'name' : data['name'],
            'hqAddress' : data['hqAddress'],
            'logoUrl' : data['logoUrl']
            }

    except KeyError:
        return utils.util_response(400,
                                   "incorrect format. Fields include name, hqAddress and logoUrl", role)


    null_fields = utils.check_null(new_political_party)
    if not null_fields:
        message = ""
        if PARTY.get_party_by_name(data.get('name')):
            #party already exists
            message = "A party already exists with that name"

        if not message:
            created_party = PARTY.create_party(**utils.sanitise(new_political_party))
            if created_party:
                created_party = utils.desanitise(created_party)
                return utils.util_response(201, created_party, role)

        return utils.util_response(409, message, role)
    return utils.util_response(400, "incorrect format. Please provide valid fields for: {}"
                               .format(", ".join(null_fields)),role)

@v1_bp.route('/parties', methods=['GET'])
def get_all_political_parties():
    """route to view all political parties"""
    role = "parties"
    all_parties = PARTY.get_all_parties()

    if all_parties:
        all_parties = [utils.desanitise(party) for party in all_parties]
        return utils.util_response(200, all_parties, role)
    return utils.util_response(404, "parties not found", role)

@v1_bp.route("/parties/<int:party_id>", methods=['GET'])
def get_specific_political_party(party_id):
    """"route to get specific political party"""
    role = "party"
    party = PARTY.get_party_by_id(party_id)
    if party:
        party = utils.desanitise(party)
        return utils.util_response(200, party, role)
    return utils.util_response(404, "Party not found", role)

@v1_bp.route("/parties/<int:party_id>/name", methods=["PATCH"])
def edit_specific_political_party(party_id):
    """endpoint to edit specific political party"""
    role = "party"
    valid_fields = ['name']
    data = request.get_json(force=True)

    if valid_fields == list(data.keys()):
        updated_name = data['name']
        #check if name is a string
        validator = utils.Validator()
        if not validator.is_str(updated_name):
            return utils.util_response(400, "Please enter a valid name", role)

        party = utils.desanitise(PARTY.get_party_by_id(party_id))
        if party:
            party['name'] = updated_name
            response = PARTY.update_party(**utils.sanitise(party))
            if response:
                return utils.util_response(200, response, role)
        return utils.util_response(404, "party not found", role)
    
    return utils.util_response(400, "incorrect format. " +
                                       "Fields include name", role)

@v1_bp.route("/parties/<int:party_id>", methods=['DELETE'])
def delete_political_party(party_id):
    role = "party"
    """"route to delete specific political party"""
    party_deleted = PARTY.delete_party_by_id(party_id)
    if party_deleted:
        return utils.util_response(200, {"message":"Party deleted successfully"}, role)
    return utils.util_response(404, "Party not found", role)
