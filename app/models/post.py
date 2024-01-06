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
    photo_url: Optional[str] = None,
    _id: Optional[ObjectId] = None,
    created_at: Optional[datetime] = None,
    updated_at: Optional[datetime] = None
  ) -> None:
    self._id = _id
    self.title = title
    self.body = body
    self.photo_url = photo_url
    self.author_id = author_id
    self.created_at = created_at or datetime.utcnow()
    self.updated_at = updated_at


  def save(self) -> None:
    mongo = current_app.mongo

    result = mongo.db.posts.insert_one(self.to_dict())
    self._id = result.inserted_id


  def delete(self) -> None:
    mongo = current_app.mongo

    mongo.db.posts.delete_one({'_id': self._id})


  def update(self, title: str, body: str, photo_url: Optional[str] = None) -> None:
    mongo = current_app.mongo

    updated_data = {
      self.title: title,
      self.body: body,
      self.updated_at: datetime.utcnow(),
    }

    if photo_url is not None:
      updated_data.photo_url = photo_url
      # TODO: Delete previous photo

    mongo.db.posts.update_one(
      {'_id': self._id},
      {'$set': updated_data}
    )


  def to_dict(self) -> Dict[str, any]:
    post_dict = {
      'title': self.title,
      'body': self.body,
      'author_id': self.author_id,
      'photo_url': self.photo_url,
      'created_at': self.created_at,
      'updated_at': self.updated_at,
    }

    if self._id is not None:
      post_dict._id = self._id

    return post_dict


  def to_json(self) -> Dict[str, any]:
    return {
      '_id': str(self._id) if self._id else None,
      'title': self.title,
      'body': self.body,
      'author_id': str(self.author_id),
      'photo_url': self.photo_url,
      'created_at': self.created_at.isoformat() if self.created_at else None,
      'updated_at': self.updated_at.isoformat() if self.updated_at else None,
    }


  @classmethod
  def fetch_all(cls) -> List['Post']:
    mongo = current_app.mongo

    posts = mongo.db.posts.find()
    post_list = [cls(**post) for post in posts]
    return post_list


  @classmethod
  def find_posts_by_author(cls, author_id: str) -> List['Post']:
    mongo = current_app.mongo

    posts = mongo.db.posts.find({'author_id': ObjectId(author_id)})
    post_list = [cls(**post) for post in posts]
    return post_list


  @classmethod
  def find_post_by_id(cls, _id: str) -> Optional['Post']:
    mongo = current_app.mongo

    post = mongo.db.posts.find_one({'_id': ObjectId(_id)})

    if post:
      return cls(**post)

    return None


  def __repr__(self) -> str:
    return f'Post: {self.title}'