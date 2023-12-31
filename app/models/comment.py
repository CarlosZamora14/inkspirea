from datetime import datetime
from typing import Optional, List, Dict

from flask import current_app
from flask_pymongo import ObjectId


class Comment:
  def __init__(
    self,
    content: str,
    post_id: ObjectId,
    author_id: ObjectId,
    _id: ObjectId = None,
    created_at: Optional[datetime] = None,
    updated_at: Optional[datetime] = None
  ) -> None:
    self._id = _id
    self.content = content
    self.post_id = post_id
    self.author_id = author_id
    self.created_at = created_at or datetime.utcnow()
    self.updated_at = updated_at


  def save(self) -> None:
    mongo = current_app.mongo

    result = mongo.db.comments.insert_one(self.to_dict())
    self._id = result.inserted_id


  def update(self, content: str) -> None:
    mongo = current_app.mongo

    self.content = content
    self.updated_at = datetime.utcnow()

    mongo.db.comments.update_one(
      {'_id': self._id},
      {
        '$set': {
          'content': self.content,
          'updated_at': self.updated_at,
        }
      }
    )


  def to_dict(self) -> Dict[str, any]:
    comment_dict = {
      'content': self.content,
      'post_id': self.post_id,
      'author_id': self.author_id,
      'created_at': self.created_at,
      'updated_at': self.updated_at,
    }

    if self._id is not None:
      comment_dict['_id'] = self._id

    return comment_dict


  def to_json(self) -> Dict[str, any]:
    return {
      '_id': str(self._id) if self._id else None,
      'content': self.content,
      'post_id': str(self.post_id),
      'author_id': str(self.author_id),
      'created_at': self.created_at.isoformat() if self.created_at else None,
      'updated_at': self.updated_at.isoformat() if self.updated_at else None,
    }


  @classmethod
  def find_comments_by_author(cls, author_id: str) -> List['Comment']:
    mongo = current_app.mongo

    comments = mongo.db.comments.find({'author_id': ObjectId(author_id)})
    comment_list = [cls(**comment) for comment in comments]
    return comment_list


  @classmethod
  def find_comments_by_post(cls, post_id: str) -> List['Comment']:
    mongo = current_app.mongo

    comments = mongo.db.comments.find({'post_id': ObjectId(post_id)})
    comment_list = [cls(**comment) for comment in comments]
    return comment_list


  @classmethod
  def find_comment_by_id(cls, _id: str) -> Optional['Comment']:
    mongo = current_app.mongo

    comment = mongo.db.comments.find_one({'_id': ObjectId(_id)})

    if comment:
      return cls(**comment)

    return None


  @classmethod
  def count_comments_by_post(cls, post_id: str | ObjectId) -> int:
    mongo = current_app.mongo

    if (isinstance(post_id, str)):
      post_id = ObjectId(post_id)

    count = mongo.db.comments.count_documents({'post_id': post_id})

    return count


  def __repr__(self) -> str:
    return f'Comment: {self.content}'