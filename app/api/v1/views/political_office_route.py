""""defines implementation to routes for political offices"""
from flask import request, make_response
from app.api.v1.models.political_office_model import PoliticalOffice
from . import v1_bp
from . import jsonify
from . import utils

OFFICE = PoliticalOffice()
@v1_bp.route("/offices", methods=['POST'])
def create_offices():
    """creates an office and adds to the list of offices in OFFICE object
        first checks whether it exists
    """
    data = request.get_json(force=True)
    sample_data = {
        "id":12,
        "type": "office type",
        "name": "office name"
    }
    valid_fields = sample_data.keys()
    response = {}

    if utils.check_valid_fields(data, valid_fields) is False:
        response = {
            "status":400,
            "error": "incorrect format, please provide valid fields. {}"
                     .format(", ".join(valid_fields))
        }
    if (response == {}) and utils.check_valid_type(data, sample_data):
        response = {
            "status":400,
            "error": "incorrect format, please provide valid types for. {}".format(
                ", ".join(
                    ["{}:{}".format(key, type(value)) for key, value in sample_data.items()]
                    )
                )
        }
    if response != {}:
        return utils.util_response(response.get('status'), response.get('error'))

    created_office = OFFICE.create_office(**data)
    if created_office:
        return utils.util_response(201, created_office)
    return utils.util_response(409, "office already exists")

@v1_bp.route("/offices", methods=['GET'])
def get_all_offices():
    """endpoint to make a get request for offices"""
    offices = OFFICE.Offices
    if offices:
        return make_response(
            jsonify(utils.wrap_response(200, offices)), 200
            )
    return make_response(
        jsonify(utils.wrap_response(404, "offices not found")), 404
    )

@v1_bp.route("/offices/<int:office_id>", methods=['GET'])
def get_single_office(office_id):
    """endpoint to make a get request for only one office"""
    found_office = [office for office in OFFICE.Offices if office['id'] == office_id]
    if found_office:
        return utils.util_response(200, found_office)
    return utils.util_response(400, "office not found")
