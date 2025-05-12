from flask import Flask, request, jsonify
from routes.users import users_bp  # Import the users Blueprint
from routes.posts import posts_bp  # Import the posts Blueprint
from routes.comments import comments_bp  # Import the comments Blueprint

app = Flask(__name__)

# Register the Blueprints with a URL prefix
app.register_blueprint(users_bp, url_prefix='/api')
app.register_blueprint(posts_bp, url_prefix='/api')
app.register_blueprint(comments_bp, url_prefix='/api')

# Route: Homepage
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flask & Neo4j API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            ul { line-height: 1.8; }
            a { text-decoration: none; color: #007BFF; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Welcome to the Flask & Neo4j API</h1>
        <p>Use the following routes to interact with the API:</p>
        <ul>
            <li><a href="/api/users">/api/users</a> - Manage users</li>
            <li><a href="/api/users/&lt;user_id&gt;/posts">/api/users/&lt;user_id&gt;/posts</a> - Manage posts for a user</li>
            <li><a href="/api/posts/&lt;post_id&gt;/comments">/api/posts/&lt;post_id&gt;/comments</a> - Manage comments for a post</li>
        </ul>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
