from flask import render_template, flash, redirect, url_for, request
from app import db
from flask_login import current_user, login_required
from app.main.forms import UserEditForm
from app.models import User
from app.main import bp


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('main/index.html', title='Home')


@bp.route('/user/<name>')
@login_required
def user(name):
    user = User.query.filter_by(name=name).first_or_404()
    return render_template('main/user.html', user=user)


@bp.route('/user/<name>/edit', methods=['GET', 'POST'])
@login_required
def user_edit(name):
    form = UserEditForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.user_edit'))
    elif request.method == 'GET':
        if current_user.name == name:
            form.name.data = current_user.name
        else:
            return redirect(url_for('main.user', name=name))
    return render_template('main/user_edit.html', title='User Edit', form=form)
