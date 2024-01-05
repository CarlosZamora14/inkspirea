from datetime import datetime
from typing import Optional, List, Dict

from flask import current_app
from flask_pymongo import ObjectId


class Like:
  def __init__(
    self,
    user_id: ObjectId,
    post_id: ObjectId,
    _id: ObjectId = None,
    created_at: Optional[datetime] = None,
  ) -> None:
    self._id = _id
    self.user_id = user_id
    self.post_id = post_id
    self.created_at = created_at or datetime.utcnow()


  def save(self) -> None:
    mongo = current_app.mongo

    result = mongo.db.likes.insert_one(self.to_dict())
    self._id = result.inserted_id


  def delete(self) -> None:
    mongo = current_app.mongo

    mongo.db.likes.delete_one({'_id': self._id})


  def to_dict(self) -> Dict[str, any]:
    like_dict = {
      'user_id': self.user_id,
      'post_id': self.post_id,
      'created_at': self.created_at,
    }

    if self._id is not None:
      like_dict._id = self._id

    return like_dict


  @classmethod
  def find_likes_by_user(cls, user_id: str) -> List['Like']:
    mongo = current_app.mongo

    likes = mongo.db.likes.find({'user_id': ObjectId(user_id)})
    like_list = [cls(**like) for like in likes]
    return like_list


  @classmethod
  def find_like_by_id(cls, _id: str) -> 'Like':
    mongo = current_app.mongo

    like = mongo.db.likes.find_one({'_id': ObjectId(_id)})

    if like:
      return cls(**like)

    return None


  @classmethod
  def count_likes_by_post(cls, post_id: str) -> int:
    mongo = current_app.mongo

    count = mongo.db.likes.count_documents({'post_id': ObjectId(post_id)})

    return count


  def __repr__(self) -> str:
    return f'Like: {self._id}'