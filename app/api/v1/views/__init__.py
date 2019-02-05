from flask import Blueprint, jsonify

v1_bp = Blueprint('v1_bp', __name__, url_prefix="/api/v1")

@v1_bp.route("/", methods=['GET'])
def home():
    return jsonify({
        "status":200,
        "data": [{
            "message":"Welcome to Politico"
        }]
    }), 200