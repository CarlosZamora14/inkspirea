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
  JWT_TOKEN_LOCATION = 'cookies'
  JWT_CSRF_IN_COOKIES = True

  JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3600)  # 1 hour
  JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
  JWT_ACCESS_CSRF_COOKIE_NAME = 'csrf_access_token'
  JWT_ACCESS_CSRF_HEADER_NAME = 'X-CSRF-TOKEN'

  JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # 30 days
  JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'


class ProductionConfig(Config):
  DEBUG = False
  TESTING = False
  JWT_COOKIE_SECURE = True


class DevelopmentConfig(Config):
  JWT_COOKIE_SECURE = False