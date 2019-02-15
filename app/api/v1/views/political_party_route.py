""""defines implementation to routes for political parties"""
from flask import request
from app.api.v1.models.political_party_model import PoliticalParty
from . import v1_bp
from . import utils

PARTY = PoliticalParty()

@v1_bp.route('/parties', methods=['POST'])
@utils.check_fields(request, ['name', 'hqAddress', 'logoUrl'])
def create_political_party():
    """route to create a political party"""
    role = "party"
    new_political_party = dict()
    response = dict()
    data = request.get_json()

    new_political_party = {
        'name' : data['name'],
        'hqAddress' : data['hqAddress'],
        'logoUrl' : data['logoUrl']
        }
    validator = utils.PartyValidator(**new_political_party)
    errors = validator.validate()
    if errors:
        response = dict(status=400, data=errors[0])

    elif PARTY.get_party_by_name(data.get('name')):
        #party already exists
        message = "A party already exists with that name"
        response = dict(status=409, data=message)

    else:
        #party doesn't exist, create the party
        created_party = PARTY.create_party(**utils.sanitise(new_political_party))
        created_party = utils.desanitise(created_party)
        response = dict(status=201, data=created_party)

    return utils.util_response(response.get('status'), response.get('data'), role)

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
@utils.check_fields(request, ['name', 'hqAddress', 'logoUrl'])
def edit_specific_political_party(party_id):
    """endpoint to edit specific political party"""
    role = "party"
    response = dict()

    data = request.get_json()

    new_data = dict(name=data['name'], hqAddress=data['hqAddress'], logoUrl=data['logoUrl'])
    validator = utils.PartyValidator(**new_data)
    errors = validator.validate()

    if errors:
        response = dict(status=400, data=errors[0])

    else:
        party = PARTY.get_party_by_id(party_id)
        party = utils.desanitise(party)
        if party:
            new_data['id'] = party['id']
            result = PARTY.update_party(**utils.sanitise(new_data))
            if result.get('message'):
                response = dict(status=400, data=result.get('message'))

            else:
                response = dict(status=200, data=utils.desanitise(result))
        else:
            response = dict(status=404, data="party not found")

    return utils.util_response(response.get('status'), response.get('data'), role)

@v1_bp.route("/parties/<int:party_id>", methods=['DELETE'])
def delete_political_party(party_id):
    """"route to delete specific political party"""
    role = "party"
    party_deleted = PARTY.delete_party_by_id(party_id)
    if party_deleted:
        return utils.util_response(200, {"message":"Party deleted successfully"}, role)
    return utils.util_response(404, "Party not found", role)
