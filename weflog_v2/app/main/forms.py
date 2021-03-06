from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class NameForm(Form):
    name = StringField('Enter your name below', validators=[Required()])
    submit = SubmitField('Submit')
