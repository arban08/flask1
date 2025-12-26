from flask import Flask
from flask_cors import CORS #type: ignore
from .db import db
from .routes.comments import comments_bp
from .routes.tasks import tasks_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    CORS(app)
    db.init_app(app)

    app.register_blueprint(comments_bp, url_prefix="/api/comments")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")

    # Add this root route here
    @app.route("/")
    def home():
        return "Flask backend is running!"

    # Create tables
    with app.app_context():
        db.create_all()

    return app