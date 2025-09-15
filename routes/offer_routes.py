from flask import Blueprint,jsonify


offer_blueprint = Blueprint("offer_blueprint",__name__)

@offer_blueprint.route("/offer",methods=["POST"])
def create_offer():
    return jsonify({"message":"offer created successfully"})