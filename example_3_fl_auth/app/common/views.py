from flask import (
    Blueprint,
    render_template,
)

from flask_login import login_required, current_user

common = Blueprint('common', __name__)


@common.route('/')
@common.route('/home')
def home():
    return render_template('home.html')


@common.route('/user_info')
@login_required
def user_info():
    return f'User info: [{current_user.id}]:{current_user.username}'
