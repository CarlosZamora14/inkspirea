from flask import (
  render_template,
  Blueprint,
  flash,
  redirect,
  request,
  url_for,
  make_response,
  g,
  current_app,
)
from flask_jwt_extended import (
  jwt_required,
  create_access_token,
  create_refresh_token,
  get_jwt_identity,
  set_access_cookies,
  set_refresh_cookies,
  decode_token,
  unset_refresh_cookies,
  unset_jwt_cookies,
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.user import User
from app.helpers.url_utilities import decode_next_url

auth = Blueprint('auth', __name__)


@auth.before_app_request
def load_logged_in_user():
  try:
    access_token = request.cookies.get(current_app.config.get('JWT_ACCESS_COOKIE_NAME'))
    jwt_data = decode_token(access_token)
    g.user = User.find_by_id(jwt_data.get('sub'))
  except:
    pass


@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    # Validating that the username and password are not empty
    # TODO: Implement more robust validation
    error = None
    if not username or not username.strip():
      error = 'Username is required'
    elif not password or not password.strip():
      error = 'Password is required'

    # Querying database
    if not error:
      user = User.find_by_username(username)

      if user is None or not check_password_hash(user.password, password):
        error = 'Invalid credentials'


    if error is None:
      next_url = decode_next_url(request.args.get('next'))

      location = next_url or url_for('blog.index')

      response = make_response(redirect(location))
      set_cookies(response, str(user._id))

      return response


    flash(error)

  return render_template('auth/login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    # Validating that the username and password are not empty
    # TODO: Implement more robust validation
    error = None
    if not username or not username.strip():
      error = 'Username is required'
    elif not password or not password.strip():
      error = 'Password is required'

    # Querying database
    if error is None:
      user = User.find_by_username(username)

      if user is None:
        new_user = User(username, generate_password_hash(password))
        new_user.save()
      else:
        error = f'The username {username} is already taken'


    if error is None:
      return redirect(url_for('auth.login'))


    flash(error)

  return render_template('auth/signup.html')


@auth.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh_access_token():
  next_url = decode_next_url(request.args.get('next'))
  current_user = get_jwt_identity()

  location = next_url or url_for('blog.index')

  response = make_response(redirect(location))
  set_cookies(response, current_user)

  return response


@auth.route('/logout', methods=['GET'])
@jwt_required()
def logout():
  response = make_response(redirect(url_for('auth.login')))

  g.user = None
  unset_jwt_cookies(response)
  unset_refresh_cookies(response)

  return response


# Helpers
def set_cookies(response, current_user: str) -> None:
  access_token = create_access_token(identity=current_user)
  refresh_token = create_refresh_token(identity=current_user)

  set_access_cookies(response, access_token)
  set_refresh_cookies(response, refresh_token)