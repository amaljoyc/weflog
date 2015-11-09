from flask import render_template, session, redirect, url_for, flash
from .. import db
from ..models import User
from . import main
from .forms import NameForm

from datetime import datetime


@main.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@main.route('/name-form', methods=['GET', 'POST'])
def name_form():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        db_user = User.query.filter_by(username=session.get('name')).first()
        if db_user is None:
            db_user = User(username=session.get('name'))
            db.session.add(db_user)
            db.session.commit()
            flash('You are a new user.')
        else:
            flash('You are an existing user.')
        return redirect(url_for('.name_form'))
    return render_template(
        'name-form.html', form=form, name=session.get('name'))


@main.route('/<name>')
def user(name):
    return render_template('user.html', username=name)
