import json
from app import create_app
from app.db import db
import pytest

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_add_comment(client):
    response = client.post(
        "/api/comments/",
        data=json.dumps({"content": "Test comment", "task_id": 1}),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_update_comment(client):
    create_response = client.post(
        "/api/comments/",
        data=json.dumps({"content": "Old", "task_id": 1}),
        content_type="application/json"
    )

    comment_id = create_response.get_json()["id"]

    response = client.put(
        f"/api/comments/{comment_id}",
        data=json.dumps({"content": "Updated"}),
        content_type="application/json"
    )

    assert response.status_code == 200
    assert response.get_json()["content"] == "Updated"

def test_delete_comment(client):
    create_response = client.post(
        "/api/comments/",
        data=json.dumps({"content": "Delete me", "task_id": 1}),
        content_type="application/json"
    )

    comment_id = create_response.get_json()["id"]

    response = client.delete(f"/api/comments/{comment_id}")

    assert response.status_code == 200