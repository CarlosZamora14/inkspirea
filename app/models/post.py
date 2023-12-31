from datetime import datetime
from typing import Optional, List, Dict

from flask import current_app
from flask_pymongo import ObjectId


class Post:
  def __init__(
    self,
    title: str,
    body: str,
    author_id: ObjectId,
    _id: ObjectId = None,
    created_at: Optional[datetime] = None
  ) -> None:
    self._id = _id
    self.title = title
    self.body = body
    self.author_id = author_id
    self.created_at = created_at or datetime.utcnow()


  def save(self) -> None:
    mongo = current_app.mongo

    result = mongo.db.posts.insert_one(self.to_dict())
    self._id = result.inserted_id


  def to_dict(self) -> Dict[str, any]:
    dict = {
      'title': self.title,
      'body': self.body,
      'author_id': self.author_id,
      'created_at': self.created_at,
    }

    if self._id is not None:
      dict['_id'] = self._id

    return dict


  @classmethod
  def find_posts_by_author(cls, author_id: ObjectId) -> List['Post']:
    mongo = current_app.mongo

    posts = mongo.db.posts.find({'author_id': author_id})
    post_list = [Post(**post) for post in posts]
    return post_list


  def __repr__(self) -> str:
    return f'Post: {self.title}'