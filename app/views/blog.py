from flask import render_template, Blueprint, request, url_for, redirect, flash, jsonify
from flask_jwt_extended import jwt_required, get_current_user

from app.models.post import Post


blog = Blueprint('blog', __name__)


@blog.route('/', methods=['GET'])
@jwt_required()
def index():
  posts = Post.fetch_all()
  return render_template('blog/index.html', posts=posts)


@blog.route('/create', methods=['GET', 'POST'])
@jwt_required()
def create_post():
  if request.method == 'POST':
    title = request.form.get('title')
    body = request.form.get('body')

    error = None
    if not title or not title.strip():
      error = 'Title is required'
    elif not body or not body.strip():
      error = 'Body is required'


    if error is None:
      author = get_current_user()
      new_post = Post(title, body, author._id)
      new_post.save()
      return jsonify(new_post.to_json()), 201
    else:
      return jsonify(error=error), 400

    flash(error)


  return render_template('blog/create.html')


@blog.route('/update/<post_id>', methods=['GET', 'POST'])
@jwt_required()
def update_post(post_id):
  post = Post.find_post_by_id(post_id)

  if request.method == 'POST':
    title = request.form.get('title')
    body = request.form.get('body')

    error = None
    if not title or not title.strip():
      error = 'Title is required'
    elif not body or not body.strip():
      error = 'Body is required'


    if error is None:
      author = get_current_user()
      new_post = Post(title, body, author._id)
      new_post.save()
      return jsonify(new_post.to_json()), 201
    else:
      return jsonify(error=error), 400

    flash(error)


  return render_template('blog/update.html', post=post)