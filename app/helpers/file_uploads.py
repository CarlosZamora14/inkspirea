import os

import uuid
from typing import Optional

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask import current_app, url_for


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def is_allowed_file(filename: str):
  if '.' in filename:
    extension = filename.split('.').pop()
    return extension.lower() in ALLOWED_EXTENSIONS

  return False


def upload_file(file: Optional[FileStorage]) -> str | None:
  if file and is_allowed_file(file.filename):
    filename = str(uuid.uuid4()) + secure_filename(file.filename)
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return url_for('blog.download_file', name=filename)