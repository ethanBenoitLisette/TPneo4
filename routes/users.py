from flask import Blueprint, request, jsonify
from models import create_user, get_all_users  # Import get_all_users
from neo4j import GraphDatabase

users_bp = Blueprint('users', __name__)
driver = GraphDatabase.driver("bolt://localhost:9001", auth=("neo4j", "ui"))

@users_bp.route('/users', methods=['POST'])
def add_user():
    data = request.json
    user = create_user(data['name'], data['email'])
    return jsonify({"message": "User created", "user": dict(user)}), 201

@users_bp.route('/users', methods=['GET'])
def get_users():
    users = get_all_users()  # Fetch all users
    return jsonify({"users": [dict(user) for user in users]})  # Return as JSON

@users_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    with driver.session() as session:
        result = session.run("MATCH (u:User {id: $user_id}) RETURN u", user_id=user_id)
        user = result.single()
        if user:
            user_data = user["u"]
            return jsonify({
                "id": user_data["id"],
                "name": user_data["name"],
                "email": user_data["email"],
                "created_at": user_data["created_at"]
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404

@users_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    with driver.session() as session:
        result = session.run("MATCH (u:User {id: $user_id}) DETACH DELETE u RETURN u", user_id=user_id)
        if result.consume().counters.nodes_deleted > 0:
            return jsonify({"message": "User deleted"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
