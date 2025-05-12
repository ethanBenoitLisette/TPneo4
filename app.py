from flask import Flask
from routes.users import users_bp
from routes.posts import posts_bp
from routes.comments import comments_bp

app = Flask(__name__)

# Enregistrer les routes
app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(comments_bp)

if __name__ == '__main__':
    app.run(debug=True)
