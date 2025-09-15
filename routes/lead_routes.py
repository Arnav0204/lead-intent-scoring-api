from flask import Blueprint,jsonify


lead_blueprint = Blueprint("lead_blueprint",__name__)

@lead_blueprint.route("/leads/upload",methods=["POST"])
def create_leads():
    return jsonify({"message":"leads uploaded successfully"})