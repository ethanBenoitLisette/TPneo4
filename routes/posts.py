from flask import Blueprint, request, jsonify
from models import create_post, get_all_posts  # Import get_all_posts
from neo4j import GraphDatabase

posts_bp = Blueprint('posts', __name__)
driver = GraphDatabase.driver("bolt://localhost:9001", auth=("neo4j", "ui"))

@posts_bp.route('/users/<user_id>/posts', methods=['POST'])
def add_post(user_id):
    data = request.json
    post = create_post(user_id, data['title'], data['content'])
    if post:
        return jsonify({"message": "Post created", "post": dict(post)}), 201
    return jsonify({"error": "User not found"}), 404

@posts_bp.route('/posts', methods=['GET'])
def get_posts():
    posts = get_all_posts()  # Fetch all posts
    return jsonify({"posts": [dict(post) for post in posts]})  # Return as JSON

@posts_bp.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    with driver.session() as session:
        result = session.run("MATCH (p:Post {id: $post_id}) RETURN p", post_id=post_id)
        post = result.single()
        if post:
            post_data = post["p"]
            return jsonify({
                "id": post_data["id"],
                "title": post_data["title"],
                "content": post_data["content"],
                "created_at": post_data["created_at"]
            }), 200
        else:
            return jsonify({"error": "Post not found"}), 404

@posts_bp.route('/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    with driver.session() as session:
        result = session.run("MATCH (p:Post {id: $post_id}) DETACH DELETE p RETURN p", post_id=post_id)
        if result.consume().counters.nodes_deleted > 0:
            return jsonify({"message": "Post deleted"}), 200
        else:
            return jsonify({"error": "Post not found"}), 404
