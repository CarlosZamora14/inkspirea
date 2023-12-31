from flask import render_template, Blueprint
from flask_jwt_extended import jwt_required


blog = Blueprint('blog', __name__)


@blog.route('/', methods=['GET'])
@jwt_required(locations=['cookies'])
def index():
  return render_template('blog/index.html')