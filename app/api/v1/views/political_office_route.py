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
    error_response = {}

    if utils.check_valid_fields(data, valid_fields):
        if not utils.check_valid_type(data, sample_data):
            created_office = OFFICE.create_office(**data)
            if created_office:
                return make_response(
                    jsonify(utils.wrap_response(201, created_office)), 201
                )
            return make_response(
                jsonify(utils.wrap_response(409, "office already exists"))
            )
        else:
            error_response = {
                "status":400,
                "error": "incorrect format, please provide valid types for. {}".format(
                    ", ".join(
                        ["{}:{}".format(key, type(value)) for key, value in sample_data.items()]
                        )
                    )
            }
    else:
        error_response = {
            "status":400,
            "error": "incorrect format, please provide valid fields. {}".format(", ".join(valid_fields)) 
        }
    return make_response(
        jsonify(error_response) , error_response.get('status')
    )

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
    found_office = [office for office in OFFICE.Offices if office['id'] == office_id][0]
    if found_office:
        return make_response(
            jsonify(utils.wrap_response(200, found_office)), 200
        )
    return make_response(
        jsonify(utils.wrap_response(404, "office not found")), 404
    )
