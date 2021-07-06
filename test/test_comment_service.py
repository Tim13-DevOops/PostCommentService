from app.app import app
from app.repository.database import db
from app.repository.post_comment_db import PostComment
import pytest
from datetime import datetime
from test.tokens import user1_token
import json

def populate_db():

    comment = PostComment(
        timestamp=datetime(2000, 5, 5, 5, 5, 5, 5),
        post_id=1,
        profile_username="user2panda",
        text="comment1"
    )
    db.session.add(comment)

    comment = PostComment(
        timestamp=datetime(2000, 5, 5, 5, 5, 5, 5),
        post_id=2,
        profile_username="user2panda",
        text="comment2"
    )
    db.session.add(comment)
    
    comment = PostComment(
        timestamp=datetime(2000, 5, 5, 5, 5, 5, 5),
        post_id=1,
        profile_username="user3panda",
        text="comment3"
    )
    db.session.add(comment)
    
    db.session.commit()

@pytest.fixture
def client():
    app.config["TESTING"] = True

    db.create_all()

    populate_db()

    with app.app_context():
        with app.test_client() as client:
            yield client

    db.session.remove()
    db.drop_all()


def test_get_comments_happy(client):
    result = client.get("/post/1")

    assert len(result.json) == 2

def test_post_comment_happy(client):
    comment_dict = {
        'text': 'sve lepo'
    }

    result = client.post("/post/1", data=json.dumps(comment_dict), content_type="application/json", headers={"Authorization": "Bearer " + user1_token})

    assert result.json["id"] == 4
    assert result.json["text"] == 'sve lepo'
    assert result.json["profile_username"] == 'user1panda'
    assert result.json["deleted"] == False
    assert result.json["timestamp"] != None
    assert result.json["post_id"] == 1


def test_post_comments_sad(client):
    comment_dict = {
        'text': 'sve lepo'
    }

    result = client.post("/post/1", data=json.dumps(comment_dict), headers={"Authorization": "Bearer " + user1_token})

    assert result.status_code == 500
