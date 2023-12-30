from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

from app.views.auth import auth
from app.views.blog import blog


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
  app.register_blueprint(auth)
  app.register_blueprint(blog)


  # JWT error handlers
  @jwt.expired_token_loader
  def expired_token_callback(jwt_header, jwt_data):
    return jsonify(message='Token has expired', error='token_expired'), 401


  @jwt.invalid_token_loader
  def invalid_token_callback(error):
    return jsonify(message='Signature verification failed', error='invalid_token'), 401


  @jwt.unauthorized_loader
  def missing_token_callback(error):
    return jsonify(message='Request does not contain a token', error='authorization_header'), 401


  return app