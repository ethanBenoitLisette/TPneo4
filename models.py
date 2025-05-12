from py2neo import Node, Relationship
from config import graph
import uuid
from datetime import datetime

def create_user(name, email):
    user_id = str(uuid.uuid4())
    user = Node("User", id=user_id, name=name, email=email, created_at=str(datetime.utcnow()))
    graph.create(user)
    return user

def create_post(user_id, title, content):
    user = graph.nodes.match("User", id=user_id).first()
    if not user:
        return None
    post_id = str(uuid.uuid4())
    post = Node("Post", id=post_id, title=title, content=content, created_at=str(datetime.utcnow()))
    rel = Relationship(user, "CREATED", post)
    graph.create(post | rel)
    return post

def create_comment(user_id, post_id, content):
    user = graph.nodes.match("User", id=user_id).first()
    post = graph.nodes.match("Post", id=post_id).first()
    if not user or not post:
        return None
    comment_id = str(uuid.uuid4())
    comment = Node("Comment", id=comment_id, content=content, created_at=str(datetime.utcnow()))
    rel1 = Relationship(user, "CREATED", comment)
    rel2 = Relationship(post, "HAS_COMMENT", comment)
    graph.create(comment | rel1 | rel2)
    return comment

def get_all_users():
    users = []
    for user in graph.nodes.match("User"):
        users.append({
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "created_at": user["created_at"]
        })
    return users

def get_all_posts():
    posts = []
    for post in graph.nodes.match("Post"):
        posts.append({
            "id": post["id"],
            "title": post["title"],
            "content": post["content"],
            "created_at": post["created_at"]
        })
    return posts

def get_all_comments():
    comments = []
    for comment in graph.nodes.match("Comment"):
        comments.append({
            "id": comment["id"],
            "content": comment["content"],
            "created_at": comment["created_at"]
        })
    return comments
