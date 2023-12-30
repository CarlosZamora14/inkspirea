from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Setting configuration
app.config.setdefault('ENV', 'development')

if app.config['ENV'] == 'production':
  app.config.from_object('config.ProductionConfig')
else:
  app.config.from_object('config.DevelopmentConfig')

jwt = JWTManager(app)
mongo = PyMongo(app)

from app.views.auth import auth
app.register_blueprint(auth)

from app.views.blog import blog
app.register_blueprint(blog)