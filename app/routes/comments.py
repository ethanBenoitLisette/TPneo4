from flask import Blueprint, request, jsonify
from app import graph
from py2neo import Node, Relationship
from datetime import datetime

comments_bp = Blueprint("comments", __name__, url_prefix="/comments")

@comments_bp.route("", methods=["GET"])
def get_all_comments():
    result = graph.run("MATCH (c:Comment) RETURN c").data()
    return jsonify([dict(r["c"]) for r in result])