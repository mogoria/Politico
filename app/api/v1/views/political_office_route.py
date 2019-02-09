""""defines implementation to routes for political offices"""
from flask import request, make_response
from app.api.v1.models.political_office_model import PoliticalOffice
from . import v1_bp
from . import jsonify
from . import utils

OFFICE = PoliticalOffice()
@v1_bp.route("/offices", methods=['POST'])
def create_offices():
    data = request.get_json(force=True)
    valid_fields = ["id", "type", "name"]
    sample_data = {
        "id":12,
        "type": "office type",
        "name": "office name"
    }
    response = {}

    if utils.check_valid_fields(data, valid_fields):
        if not utils.check_valid_type(data, sample_data):
            created_office = OFFICE.create_office(**data)
            if created_office:
                return utils.util_response(201, created_office)
            return utils.util_response(409, "office already exists")
        else:
            response = {
                "status":400,
                "error": "incorrect format, please provide valid types for. {}".format(
                    ", ".join(
                        ["{}:{}".format(key, type(value)) for key, value in sample_data.items()]
                        )
                    )
            }
    else:
        response = {
            "status":400,
            "error": "incorrect format, please provide valid fields. {}".format(", ".join(valid_fields)) 
        }
    return utils.util_response(response.get('status'), response.get('error'))

@v1_bp.route("/offices", methods=['GET'])
def get_all_offices():
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
    found_office = [office for office in OFFICE.Offices if office['id'] == office_id]
    if found_office:
        return utils.util_response(200, found_office)
    return utils.util_response(400, "office not found")
