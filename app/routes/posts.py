# app/routes/posts.py
from flask import Blueprint, request, jsonify
from app import graph
from py2neo import Node, Relationship
from datetime import datetime

posts_bp = Blueprint("posts", __name__, url_prefix="/posts")

@posts_bp.route("", methods=["GET"])
def get_all_posts():
    result = graph.run("MATCH (p:Post) RETURN p").data()
    return jsonify([dict(r["p"]) | {"id": r["p"].identity} for r in result])

@posts_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_posts(user_id):
    query = """
    MATCH (u:User)-[:CREATED]->(p:Post)
    WHERE id(u) = $user_id
    RETURN p
    """
    posts = graph.run(query, user_id=user_id).data()
    return jsonify([dict(r["p"]) | {"id": r["p"].identity} for r in posts])

@posts_bp.route("/user/<int:user_id>", methods=["POST"])
def create_post(user_id):
    data = request.json
    query = """
    MATCH (u:User) WHERE id(u) = $user_id
    CREATE (p:Post {title: $title, content: $content, created_at: $created_at})
    CREATE (u)-[:CREATED]->(p)
    RETURN p
    """
    post = graph.run(query, user_id=user_id, title=data["title"], content=data["content"], created_at=str(datetime.utcnow())).evaluate()
    return jsonify(dict(post) | {"id": post.identity}), 201

@posts_bp.route("/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    data = request.json
    query = """
    MATCH (p:Post)
    WHERE id(p) = $post_id
    SET p.title = $title, p.content = $content
    RETURN p
    """
    post = graph.run(query, post_id=post_id, title=data["title"], content=data["content"]).evaluate()
    if post:
        return jsonify(dict(post) | {"id": post.identity})
    return jsonify({"error": "Post not found"}), 404

@posts_bp.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    query = """
    MATCH (p:Post)
    WHERE id(p) = $post_id
    DETACH DELETE p
    RETURN COUNT(p) as count
    """
    result = graph.run(query, post_id=post_id).evaluate()
    if result == 0:
        return jsonify({"error": "Post not found"}), 404
    return jsonify({"message": "Post deleted"})

@posts_bp.route("/<int:post_id>/like", methods=["POST"])
def like_post(post_id):
    user_id = request.json.get("user_id")
    query = """
    MATCH (u:User), (p:Post)
    WHERE id(u) = $user_id AND id(p) = $post_id
    MERGE (u)-[:LIKES]->(p)
    RETURN p
    """
    post = graph.run(query, user_id=user_id, post_id=post_id).evaluate()
    if post:
        return jsonify({"message": "Post liked"})
    return jsonify({"error": "User or post not found"}), 404

@posts_bp.route("/<int:post_id>/like", methods=["DELETE"])
def unlike_post(post_id):
    user_id = request.json.get("user_id")
    query = """
    MATCH (u:User)-[l:LIKES]->(p:Post)
    WHERE id(u) = $user_id AND id(p) = $post_id
    DELETE l
    RETURN p
    """
    post = graph.run(query, user_id=user_id, post_id=post_id).evaluate()
    if post:
        return jsonify({"message": "Like removed"})
    return jsonify({"error": "User or post not found"}), 404

@posts_bp.route("/<int:post_id>/comments", methods=["GET"])
def get_post_comments(post_id):
    query = """
    MATCH (p:Post)-[:HAS_COMMENT]->(c:Comment)
    WHERE id(p) = $post_id
    RETURN c
    """
    comments = graph.run(query, post_id=post_id).data()
    return jsonify([dict(r["c"]) | {"id": r["c"].identity} for r in comments])

@posts_bp.route("/<int:post_id>/comments", methods=["POST"])
def create_comment(post_id):
    data = request.json
    user_id = data.get("user_id")
    query = """
    MATCH (u:User), (p:Post)
    WHERE id(u) = $user_id AND id(p) = $post_id
    CREATE (c:Comment {content: $content, created_at: $created_at})
    CREATE (u)-[:CREATED]->(c)
    CREATE (p)-[:HAS_COMMENT]->(c)
    RETURN c
    """
    comment = graph.run(query, user_id=user_id, post_id=post_id, content=data["content"], created_at=str(datetime.utcnow())).evaluate()
    return jsonify(dict(comment) | {"id": comment.identity}), 201

# --- Routes d'amitié entre utilisateurs ---
@posts_bp.route("/friends/<int:user_id>", methods=["GET"])
def get_friends(user_id):
    query = """
    MATCH (u:User)-[:FRIENDS_WITH]-(f:User)
    WHERE id(u) = $user_id
    RETURN f
    """
    friends = graph.run(query, user_id=user_id).data()
    return jsonify([dict(r["f"]) | {"id": r["f"].identity} for r in friends])

@posts_bp.route("/friends/<int:user_id>", methods=["POST"])
def add_friend(user_id):
    friend_id = request.json.get("friend_id")
    query = """
    MATCH (u:User), (f:User)
    WHERE id(u) = $user_id AND id(f) = $friend_id
    MERGE (u)-[:FRIENDS_WITH]-(f)
    RETURN f
    """
    friend = graph.run(query, user_id=user_id, friend_id=friend_id).evaluate()
    if friend:
        return jsonify({"message": "Friend added"})
    return jsonify({"error": "User not found"}), 404

@posts_bp.route("/friends/<int:user_id>/<int:friend_id>", methods=["DELETE"])
def remove_friend(user_id, friend_id):
    query = """
    MATCH (u:User)-[r:FRIENDS_WITH]-(f:User)
    WHERE id(u) = $user_id AND id(f) = $friend_id
    DELETE r
    RETURN f
    """
    friend = graph.run(query, user_id=user_id, friend_id=friend_id).evaluate()
    if friend:
        return jsonify({"message": "Friend removed"})
    return jsonify({"error": "Friendship not found"}), 404

@posts_bp.route("/friends/<int:user_id>/<int:friend_id>", methods=["GET"])
def are_friends(user_id, friend_id):
    query = """
    MATCH (u:User)-[:FRIENDS_WITH]-(f:User)
    WHERE id(u) = $user_id AND id(f) = $friend_id
    RETURN f
    """
    result = graph.run(query, user_id=user_id, friend_id=friend_id).evaluate()
    return jsonify({"are_friends": bool(result)})

@posts_bp.route("/friends/<int:user_id>/mutual/<int:other_id>", methods=["GET"])
def get_mutual_friends(user_id, other_id):
    query = """
    MATCH (u1:User)-[:FRIENDS_WITH]-(mutual:User)-[:FRIENDS_WITH]-(u2:User)
    WHERE id(u1) = $user_id AND id(u2) = $other_id
    RETURN mutual
    """
    result = graph.run(query, user_id=user_id, other_id=other_id).data()
    return jsonify([dict(r["mutual"]) | {"id": r["mutual"].identity} for r in result])
