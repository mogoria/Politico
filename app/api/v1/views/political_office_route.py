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
    try:
        new_office = {
            "id":data['id'],
            "type":data['type'],
            "name":data['name']
        }
    except KeyError:
        return make_response(
            jsonify(utils.wrap_response(400, {
                "message":"All fields are required. id, name and type"
            })), 400
        )

    created_office = OFFICE.create_office(**new_office)
    if created_office:
        return make_response(
            jsonify(utils.wrap_response(201, created_office)), 201
        )
    else:
        return make_response(
            jsonify(utils.wrap_response(409, "party already exists"))
        )