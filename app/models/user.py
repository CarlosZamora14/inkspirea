from datetime import datetime
from typing import Optional, Dict

from flask import current_app
from flask_pymongo import ObjectId


class User:
  def __init__(
    self,
    username: str,
    password: str,
    photo_url: Optional[str] = None,
    _id: Optional[ObjectId] = None,
    is_admin: bool = False,
    created_at: Optional[datetime] = None
  ) -> None:
    self._id = _id
    self.username = username
    self.password = password
    self.photo_url = photo_url
    self.is_admin = is_admin
    self.created_at = created_at or datetime.utcnow()


  def save(self) -> None:
    mongo = current_app.mongo

    result = mongo.db.users.insert_one(self.to_dict())
    self._id = result.inserted_id


  def to_dict(self) -> Dict[str, any]:
    user_dict = {
      'username': self.username,
      'password': self.password,
      'photo_url': self.photo_url,
      'is_admin': self.is_admin,
      'created_at': self.created_at,
    }

    if self._id is not None:
      user_dict._id = self._id

    return user_dict


  def to_json(self) -> Dict[str, any]:
    return {
      '_id': str(self._id) if self._id else None,
      'username': self.username,
      'password': self.password,
      'photo_url': self.photo_url,
      'is_admin': self.is_admin,
      'created_at': self.created_at.isoformat() if self.created_at else None,
    }


  @classmethod
  def find_by_username(cls, username: str) -> Optional['User']:
    mongo = current_app.mongo

    user_data = mongo.db.users.find_one({'username': username})

    if user_data:
      return cls(**user_data)

    return None


  @classmethod
  def find_by_id(cls, _id: str) -> Optional['User']:
    mongo = current_app.mongo

    user_data = mongo.db.users.find_one({'_id': ObjectId(_id)})

    if user_data:
      return cls(**user_data)

    return None


  @classmethod
  def get_dict_ids(cls) -> dict[ObjectId, str]:
    mongo = current_app.mongo

    users = mongo.db.users.find({})
    users_dict = {user.get('_id'): user.get('username') for user in users}

    return users_dict


  def __repr__(self) -> str:
    return f'User: {self.username}'