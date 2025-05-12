from flask import Blueprint, request, jsonify
from models import create_comment, get_all_comments  # Import get_all_comments
from neo4j import GraphDatabase

comments_bp = Blueprint('comments', __name__)
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

@comments_bp.route('/posts/<post_id>/comments', methods=['POST'])
def add_comment(post_id):
    data = request.json
    comment = create_comment(data['user_id'], post_id, data['content'])
    if comment:
        return jsonify({"message": "Comment added", "comment": dict(comment)}), 201
    return jsonify({"error": "User or Post not found"}), 404

@comments_bp.route('/comments', methods=['GET'])
def get_comments():
    comments = get_all_comments()  # Fetch all comments
    return jsonify({"comments": [dict(comment) for comment in comments]})  # Return as JSON

@comments_bp.route('/comments/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    if not comment_id:
        return jsonify({"error": "Comment ID is required"}), 400
    with driver.session() as session:
        result = session.run("MATCH (c:Comment {id: $comment_id}) RETURN c", comment_id=comment_id)
        comment = result.single()
        if comment:
            comment_data = comment["c"]
            return jsonify({
                "id": comment_data["id"],
                "content": comment_data["content"],
                "created_at": comment_data["created_at"]
            }), 200
        else:
            return jsonify({"error": "Comment not found"}), 404

@comments_bp.route('/comments/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    if not comment_id:
        return jsonify({"error": "Comment ID is required"}), 400
    with driver.session() as session:
        result = session.run("MATCH (c:Comment {id: $comment_id}) DETACH DELETE c RETURN c", comment_id=comment_id)
        if result.consume().counters.nodes_deleted > 0:
            return jsonify({"message": "Comment deleted"}), 200
        else:
            return jsonify({"error": "Comment not found"}), 404
