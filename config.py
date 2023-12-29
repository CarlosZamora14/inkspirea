import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
  DEBUG = True
  TESTING = True
  SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

  # MongoDB Configuration
  MONGO_URI = os.getenv('MONGO_URI')

  # JWT Configuration
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
  JWT_REFRESH_TOKEN_SECRET_KEY = os.getenv('JWT_REFRESH_TOKEN_SECRET_KEY')
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3600)  # 1 hour
  JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # 30 days

class ProductionConfig(Config):
  DEBUG = False
  TESTING = False

class DevelopmentConfig(Config):
  pass