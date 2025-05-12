from flask import Flask
from py2neo import Graph
import os

graph = None

def create_app():
    global graph
    app = Flask(__name__)
    graph = Graph(
        os.getenv("NEO4J_URL", "bolt://localhost:7687"),
        auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
    )

    from app.routes.users import users_bp
    from app.routes.posts import posts_bp
    from app.routes.comments import comments_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(comments_bp)

    return app