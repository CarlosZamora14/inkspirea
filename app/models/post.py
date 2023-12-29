from datetime import datetime
from typing import List, Dict
from bson import ObjectId
from app import mongo

class Post:
  def __init__(
    self,
    title: str,
    body: str,
    author_id: ObjectId,
    _id: ObjectId = None,
    created_at: datetime = datetime.utcnow()
  ) -> None:
    self._id = _id
    self.title = title
    self.body = body
    self.author_id = author_id
    self.created_at = created_at


  @classmethod
  def find_posts_by_author(cls, author_id: ObjectId) -> List['Post']:
    posts = mongo.db.posts.find({'author_id': author_id})
    post_list = [Post(**post) for post in posts]
    return post_list


  def __repr__(self) -> str:
    return f'Post: {self.title}'


  def to_dict(self) -> Dict[str, any]:
    return {
      '_id': self._id,
      'title': self.title,
      'body': self.body,
      'author_id': self.author_id,
      'created_at': self.created_at,
    }


  def save(self) -> None:
    result = mongo.db.posts.insert_one(self.to_dict())
    self._id = result.inserted_id