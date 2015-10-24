from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_k3y'

bootstrap = Bootstrap(app)
m = Moment(app)


class NameForm(Form):
    name = StringField('Enter your name below', validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/name-form', methods=['GET', 'POST'])
def name_form():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('name-form.html', form=form, name=name)


@app.route('/<name>')
def user(name):
    return render_template('user.html', username=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 400


if __name__ == '__main__':
    app.run(debug=True)
