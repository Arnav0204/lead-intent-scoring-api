from flask import Blueprint,jsonify


score_blueprint = Blueprint("score_blueprint",__name__)


@score_blueprint.route("/score",methods=["POST"])
def score():
    return jsonify({"message":"leads scored for given offer"})
