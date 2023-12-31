from datetime import datetime
from typing import Optional, Dict

from flask import current_app
from flask_pymongo import ObjectId


class User:
  def __init__(
    self,
    username: str,
    password: str,
    _id: ObjectId = None,
    is_admin: bool = False,
    created_at: Optional[datetime] = None
  ) -> None:
    self._id = _id
    self.username = username
    self.password = password
    self.is_admin = is_admin
    self.created_at = created_at or datetime.utcnow()


  def save(self) -> None:
    mongo = current_app.mongo

    result = mongo.db.users.insert_one(self.to_dict())
    self._id = result.inserted_id


  def to_dict(self) -> Dict[str, any]:
    dict = {
      'username': self.username,
      'password': self.password,
      'is_admin': self.is_admin,
      'created_at': self.created_at,
    }

    if self._id is not None:
      dict['_id'] = self._id

    return dict


  def to_json(self) -> Dict[str, any]:
    return {
      '_id': str(self._id),
      'username': self.username,
      'password': self.password,
      'is_admin': self.is_admin,
      'created_at': self.created_at.isoformat() if self.created_at else None,
    }


  @classmethod
  def find_by_username(cls, username: str) -> Optional['User']:
    mongo = current_app.mongo

    user_data = mongo.db.users.find_one({'username': username})

    if user_data:
      return cls(
        _id=user_data.get('_id'),
        username=user_data.get('username'),
        password=user_data.get('password'),
        is_admin=user_data.get('is_admin'),
        created_at=user_data.get('created_at'),
      )

    return None


  @classmethod
  def find_by_id(cls, _id: str) -> Optional['User']:
    mongo = current_app.mongo

    user_data = mongo.db.users.find_one({'_id': ObjectId(_id)})

    if user_data:
      return cls(
        _id=user_data.get('_id'),
        username=user_data.get('username'),
        password=user_data.get('password'),
        is_admin=user_data.get('is_admin'),
        created_at=user_data.get('created_at'),
      )

    return None


  def __repr__(self) -> str:
    return f'User: {self.username}'