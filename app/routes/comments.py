from flask import Blueprint, request, jsonify, abort
from app.db import db
from app.models import Comment

comments_bp = Blueprint("comments", __name__)

@comments_bp.route("/", methods=["POST"])
def add_comment():
    data = request.json
    comment = Comment(content=data["content"], task_id=data["task_id"])
    db.session.add(comment)
    db.session.commit()
    return jsonify({"id": comment.id, "content": comment.content}), 201


@comments_bp.route("/<int:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    if not comment:
        abort(404)
    comment.content = request.json["content"]
    db.session.commit()
    return jsonify({"id": comment.id, "content": comment.content})


@comments_bp.route("/<int:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    if not comment:
        abort(404)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted"})