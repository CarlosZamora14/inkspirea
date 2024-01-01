from flask import Flask, jsonify, redirect, url_for, request
from flask_pymongo import PyMongo, ObjectId
from flask_jwt_extended import JWTManager

from app.views.auth import auth
from app.views.blog import blog
from app.models.user import User
from app.helpers.url_utilities import (
  encode_next_url,
  decode_next_url,
  extract_base_url,
  extract_query_string_parameter,
)


def create_app():
  app = Flask(__name__)


  # Setting configuration
  if app.config.get('ENV', 'development') == 'production':
    app.config.from_object('config.ProductionConfig')
  else:
    app.config.from_object('config.DevelopmentConfig')


  # Initialize db and jwt manager
  jwt = JWTManager(app)
  mongo = PyMongo(app)

  with app.app_context():
    app.mongo = mongo


  # Register blueprints
  app.register_blueprint(auth, url_prefix='/auth')
  app.register_blueprint(blog, url_prefix='/')


  # User lookup
  @jwt.user_lookup_loader
  def user_lookup_callback(jwt_header, jwt_data):
    identity = jwt_data.get('sub')
    return User.find_by_id(identity)


  # Setting additional claims
  @jwt.additional_claims_loader
  def create_additional_claims(identity):
    user = mongo.db.users.find_one({'_id': ObjectId(identity)})

    claims = {
      'username': user.get('username'),
      'is_admin': user.get('is_admin'),
    }

    return claims


  # JWT error handlers
  @jwt.expired_token_loader
  def expired_token_callback(jwt_header, jwt_data):
    token_type = jwt_data.get('type')
    url = extract_query_string_parameter(request.url, 'next')

    next_url = decode_next_url(url) or request.url

    encoded_url = encode_next_url(extract_base_url(next_url))

    if token_type == 'access':
      return redirect(url_for('auth.refresh_access_token', next=encoded_url))

    return redirect(url_for('auth.login', next=encoded_url))


  @jwt.invalid_token_loader
  def invalid_token_callback(error):
    return jsonify(message='Signature verification failed', error=error), 401


  @jwt.unauthorized_loader
  def missing_token_callback(error):
    return jsonify(message='Unathorized request', error=error), 401


  return app