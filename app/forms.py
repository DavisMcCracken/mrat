from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, URL
from app.models import Scenario

class EntryForm(FlaskForm):
    scenario_id = SelectField('Scenario', coerce=int, validators=[DataRequired()])
    score = IntegerField('Score', validators=[DataRequired(), NumberRange(min=0)])
    proof = StringField('Proof (link to video)', validators=[Optional(), URL()])
    submit = SubmitField('Submit Score')

    def set_choices(self):
        from app.models import Scenario
        self.scenario_id.choices = [(s.id, s.name) for s in Scenario.query.order_by(Scenario.name).all()]

from wtforms import PasswordField
from wtforms.validators import EqualTo, Email

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')