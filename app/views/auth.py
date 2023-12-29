from flask import (
  render_template, g, Blueprint, flash, redirect, request, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user import User

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
      return redirect(url_for('blog.index'))

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