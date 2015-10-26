from flask import Flask, render_template, redirect, session, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy

from datetime import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_k3y'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
m = Moment(app)
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

    def __str__(self):
        return '<Role %s>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

    def __str__(self):
        return '<User %s>' % self.username


class NameForm(Form):
    name = StringField('Enter your name below', validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/name-form', methods=['GET', 'POST'])
def name_form():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        session['name'] = form.name.data
        if old_name is not None and session.get('name') != old_name:
            flash('You have successfully changed your name.')
        return redirect(url_for('name_form'))
    return render_template(
        'name-form.html', form=form, name=session.get('name'))


@app.route('/<name>')
def user(name):
    return render_template('user.html', username=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 400


if __name__ == '__main__':
    manager.run()
