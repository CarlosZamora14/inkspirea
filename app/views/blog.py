from flask import (
  render_template, g, Blueprint, flash, redirect, request, url_for
)


blog = Blueprint('blog', __name__)


@blog.route('/')
def index():
  return render_template('blog/index.html')