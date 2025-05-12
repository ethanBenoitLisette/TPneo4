from py2neo import Node, Relationship
from app import graph
from datetime import datetime

def create_user(name, email):
    user = Node("User", name=name, email=email, created_at=str(datetime.utcnow()))
    graph.create(user)
    return user

def get_user_by_id(user_id):
    return graph.evaluate("MATCH (u:User) WHERE id(u) = $id RETURN u", id=int(user_id))