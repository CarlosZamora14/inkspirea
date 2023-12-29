from flask import (
  render_template, g, Blueprint, flash, redirect, request, url_for, current_app
)

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    current_app.logger.info('The data received was %s, %s', username, password)

  return render_template('auth/login.html')