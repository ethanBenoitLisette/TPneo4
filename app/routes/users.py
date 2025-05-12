from flask import Blueprint, request, jsonify
from app import graph
from app.models import create_user, get_user_by_id
from py2neo.matching import NodeMatcher

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("", methods=["GET"])
def get_users():
    matcher = NodeMatcher(graph)
    users = list(matcher.match("User"))
    return jsonify([dict(u) | {"id": u.identity} for u in users])

@users_bp.route("", methods=["POST"])
def add_user():
    data = request.json
    user = create_user(data["name"], data["email"])
    return jsonify(dict(user) | {"id": user.identity}), 201

@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(dict(user) | {"id": user.identity})
    return jsonify({"error": "User not found"}), 404

@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        graph.delete(user)
        return jsonify({"message": "Deleted"})
    return jsonify({"error": "User not found"}), 404