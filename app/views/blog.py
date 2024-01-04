from flask import render_template, Blueprint, request, url_for, redirect, flash, jsonify
from flask_pymongo import ObjectId
from flask_jwt_extended import jwt_required, get_current_user, get_jwt_identity, current_user

from app.models.post import Post
from app.models.user import User


blog = Blueprint('blog', __name__)


@blog.route('/', methods=['GET'])
@jwt_required()
def index():
  posts = Post.fetch_all()
  users_dict = User.get_dict_ids()

  return render_template('blog/index.html', posts=posts, users_dict=users_dict)


@blog.route('/posts/<post_id>', methods=['GET'])
@jwt_required()
def show_post(post_id):
  post = Post.find_post_by_id(post_id)

  if post is None:
    return jsonify(message=f'Post with id {post_id} does not exist'), 404

  return render_template('blog/post.html', post=post)


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

  if post is None:
    return jsonify(message=f'Post with id {post_id} does not exist'), 404

  if not current_user.is_admin and current_user._id != post.author_id:
    return jsonify(message=f'This action is unauthorized'), 403

  if request.method == 'POST':
    title = request.form.get('title')
    body = request.form.get('body')

    error = None
    if not title or not title.strip():
      error = 'Title is required'
    elif not body or not body.strip():
      error = 'Body is required'


    if error is None:
      post.update(title, body)
      return jsonify(post.to_json()), 201
    else:
      return jsonify(error=error), 400

    flash(error)

  return render_template('blog/update.html', post=post)


@blog.route('/delete/<post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
  post = Post.find_post_by_id(post_id)

  if post is None:
    return jsonify(message=f'Post with id {post_id} does not exist'), 404

  if not current_user.is_admin and current_user._id != post.author_id:
    return jsonify(message=f'This action is unauthorized'), 403

  post.delete()
  return jsonify(message=f'Post with id {post_id} has been deleted', data=post.to_json()), 200