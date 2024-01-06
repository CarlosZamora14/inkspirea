from flask import render_template, Blueprint, request, url_for, redirect, flash, jsonify, send_from_directory, current_app
from flask_pymongo import ObjectId
from flask_jwt_extended import jwt_required, get_current_user, get_jwt_identity, current_user

from app.models.post import Post
from app.models.user import User
from app.models.comment import Comment
from app.models.like import Like

from app.helpers.file_uploads import upload_file

from werkzeug.exceptions import RequestEntityTooLarge


blog = Blueprint('blog', __name__)


@blog.route('/', methods=['GET'])
@jwt_required()
def index():
  posts = Post.fetch_all()
  users_dict = User.get_dict_ids()

  return render_template(
    'blog/index.html',
    posts=posts,
    users_dict=users_dict,
    count_likes=Like.count_likes_by_post,
    find_if_user_likes_post=Like.find_if_user_likes_post,
    count_comments=Comment.count_comments_by_post,
  )


@blog.route('/posts/<post_id>', methods=['GET'])
@jwt_required()
def show_post(post_id):
  post = Post.find_post_by_id(post_id)

  if post is None:
    return jsonify(message=f'Post with id {post_id} does not exist'), 404

  users_dict = User.get_dict_ids()
  comments = Comment.find_comments_by_post(post_id)
  author = User.find_by_id(post.author_id)

  print()
  print(author)
  print()

  return render_template('blog/post.html', post=post, users_dict=users_dict, comments=comments, author=author)


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
      # Handle file upload
      file_url = None

      if 'image' in request.files:
        image = request.files.get('image')

        if image.filename != '':
          file_url = upload_file(image)

      author = get_current_user()
      new_post = Post(title, body, author._id, file_url)
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
      # Handle file upload
      file_url = None

      if 'image' in request.files:
        image = request.files.get('image')

        if image.filename != '':
          file_url = upload_file(image)

      post.update(title, body, file_url)
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


@blog.route('/comments', methods=['POST'])
@jwt_required()
def post_comment():
  content = request.form.get('comment')
  post_id = request.form.get('post-id')

  if not content or not content.strip():
    return jsonify(message=f'Comment can not be empty'), 400

  post = Post.find_post_by_id(post_id)

  if not post:
    return jsonify(message=f'Post with id {post_id} does not exist'), 404

  author = get_current_user()
  new_comment = Comment(content, post._id, author._id)
  new_comment.save()

  return jsonify(new_comment.to_json()), 201


@blog.route('/likes', methods=['POST'])
@jwt_required()
def like_post():
  post_id = request.form.get('post-id')

  post = Post.find_post_by_id(post_id)

  if not post:
    return jsonify(message=f'Post with id {post_id} does not exist'), 404

  user_id = get_jwt_identity()

  like = Like.find_like_by_user_and_post(user_id, post_id)

  if like:
    like.delete()
    return jsonify(message=f'Like for post with id {post_id} deleted successfully'), 200

  new_like = Like(ObjectId(user_id), ObjectId(post_id))
  new_like.save()

  return jsonify(message=f'Like for post with id {post_id} created successfully'), 201


@blog.route('/uploads/<name>')
@jwt_required()
def download_file(name):
  return send_from_directory(current_app.config['UPLOAD_FOLDER'], name)


@blog.errorhandler(RequestEntityTooLarge)
def handle_request_entity_too_large(e):
  return jsonify(message='The file size too large, the maximum file size allowed is 16 Megabytes'), 413