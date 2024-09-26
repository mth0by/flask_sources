from flask import (
    request,
    render_template,
    flash,
    redirect,
    url_for,
    Blueprint,
    g,
)

from flask_login import current_user, login_user, logout_user, login_required
from app import login_manager, db
from app.auth.forms import LoginForm
from app.auth.models import User, UserRoles, Role

from app.auth.backends.ldap import do_login, do_logout, get_user_roles

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@auth.before_request
def get_current_user():
    g.user = current_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Авторизация уже пройдена ранее.')
        return redirect(url_for('common.home'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']

        try:
            entry = do_login(username, password)
        except Exception as ex:
            flash(str(ex), 'danger')
            return render_template('login.html', form=form)
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, password=password)
        else:
            db.session.query(UserRoles).filter_by(user_id=user.id).delete()

        user_roles = list(get_user_roles(entry))
        roles = db.session.query(Role).filter(Role.name.in_(user_roles))
        user.roles.extend(roles)
        db.session.add(user)

        db.session.commit()
        login_user(user)
        flash('Авторизация успешна.', 'success')
        return redirect(url_for('common.home'))
    if form.errors:
        flash(form.errors, 'danger')

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    do_logout()
    return redirect(url_for('common.home'))