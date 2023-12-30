from flask import (
  render_template,
  jsonify,
  Blueprint,
  flash,
  redirect,
  request,
  url_for,
  make_response,
)
from flask_jwt_extended import (
  jwt_required,
  create_access_token,
  create_refresh_token,
  get_jwt_identity,
  decode_token,
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user import User
from app import jwt

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    error = None
    if not username:
      error = 'Username is required'
    elif not password:
      error = 'Password is required'

    if not error:
      user = User.find_by_username(username)

      if user == None or not check_password_hash(user.password, password):
        error = 'Invalid credentials'

    if error != None:
      flash(error)
    else:
      additional_claims = {
        'username': user.username,
        'is_admin': user.is_admin,
      }

      access_token = create_access_token(identity=str(user._id), additional_claims=additional_claims)
      refresh_token = create_refresh_token(identity=str(user._id), additional_claims=additional_claims)

      response = make_response()
      response.set_cookie('jwt_token', value=access_token, httponly=True)
      response.set_cookie('jwt_refresh_token', value=refresh_token, httponly=True)
      return redirect(url_for('blog.index'), response=response)

  return render_template('auth/login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    error = None
    if not username:
      error = 'Username is required'
    elif not password:
      error = 'Password is required'

    if not error:
      user = User.find_by_username(username)

      if user == None:
        new_user = User(username, generate_password_hash(password))
        new_user.save()
      else:
        error = f'The username {username} is already taken'

    if error != None:
      flash(error)
    else:
      return redirect(url_for('auth.login'))

  return render_template('auth/signup.html')


@auth.route('/protected', methods=['GET'])
def protected():
  access_token = request.cookies.get('jwt_token')
  refresh_token = request.cookies.get('jwt_refresh_token')

  return jsonify(token=access_token, refresh_token=refresh_token)


@auth.route('/refresh', methods=['POST'])
def refresh():
  refresh_token = request.cookies.get('jwt_refresh_token')
  new_access_token = refresh_access_token(refresh_token)

  if new_access_token == None:
    return jsonify(msg='Invalid refresh token'), 401

  current_user = get_jwt_identity()
  new_access_token = create_access_token(identity=current_user)
  new_refresh_token = create_refresh_token(identity=current_user)
  return jsonify(access_token=new_access_token, refresh_token=new_refresh_token)


def generate_access_token(user: User) -> str:
  additional_claims = {
    'username': user.username,
    'is_admin': user.is_admin,
  }

  access_token = create_access_token(identity=str(user._id), additional_claims=additional_claims)
  return access_token


def generate_refresh_token(user: User) -> str:
  additional_claims = {
    'username': user.username,
    'is_admin': user.is_admin,
  }

  refresh_token = create_access_token(identity=str(user._id), additional_claims=additional_claims)
  return refresh_token


def refresh_access_token(refresh_token: str) -> str | None:
  try:
    payload = decode_token(refresh_token)
    user_id = payload['sub']
    new_access_token = create_access_token(identity=user_id)
    return new_access_token
  except jwt.ExpiredSignatureError:
    return None