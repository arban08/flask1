from flask import Blueprint, request, jsonify
from app.db import db
from app.models import Task

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([
        {"id": t.id, "title": t.title} for t in tasks
    ])

@tasks_bp.route("/", methods=["POST"])
def create_task():
    data = request.json
    task = Task(title=data["title"])
    db.session.add(task)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title}), 201
