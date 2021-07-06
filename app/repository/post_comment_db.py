from datetime import datetime
from .database import db
from dataclasses import dataclass


@dataclass
class PostComment(db.Model):
    id: int
    timestamp: datetime
    post_id: int
    profile_username: str
    text: str
    deleted: bool

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    text = db.Column(db.String(255))
    post_id = db.Column(db.Integer)
    profile_username = db.Column(db.String(255))
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Product {self.name}"