from datetime import datetime
from flask import abort
from app.repository.post_comment_db import PostComment
from app.repository.database import db
from app.rbac import rbac
import logging
import json


def get_comments(post_id):
    comments = PostComment.query.filter_by(post_id=post_id, deleted=False).all()
    return comments

def create_comment(post_id, comment_dict):
    user = rbac.get_current_user()
    comment_dict['profile_username'] = user.username
    comment_dict.pop("id", None)
    comment_dict['post_id'] = post_id
    comment = PostComment(**comment_dict)
    comment.timestamp = datetime.now()
    db.session.add(comment)
    db.session.commit()
    return comment