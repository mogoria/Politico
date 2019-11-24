from flask import request, jsonify, make_response
from app.api.v2.models import user_model
from . import v2_bp
from app.api.v2 import util


@v2_bp.route('/users', methods=['POST', ])
@util.check_fields(request, util.USER_FIELDS)
def create_user():
    resp = dict()
    data = request.get_json(force=True)
    errors = util.validate_user(**data).validate()
    if errors:
        return make_response(
            jsonify({
                "error": {"message": errors},
                "status": 400
            }), 400
        )
    first_name = data.get('firstname')
    last_name = data.get('lastname')
    other_name = data.get('othername')
    email = data.get('email')
    phonenumber = data.get('phonenumber')
    passporturi = data.get('passporturi')
    password = data.get('password')
    isadmin = data.get('isadmin')

    user = user_model.User(firstname=first_name,
                           lastname=last_name,
                           othername=other_name,
                           email=email,
                           phonenumber=phonenumber,
                           passporturi=passporturi,
                           password=password,
                           isadmin=isadmin)

    if user.get_user_by_email(email):
        resp = dict(error={'message': 'A user already exists with that email'},
                    status=400)
    else:
        resp = dict(data=[user.add_user()],
                    status=201,
                    )
    print("response: {}".format(resp))
    return make_response(jsonify(resp), resp.get('status'))


@v2_bp.route('/users', methods=['GET', ])
def get_all_users():
    resp = dict()
    users = user_model.User.get_all_users()
    if users:
        resp = dict(data=users,
                    status=200)
    else:
        resp = dict(message="No users found",
                    status=404)
    return make_response(jsonify(resp), resp.get('status'))
