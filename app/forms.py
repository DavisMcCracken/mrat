from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, SubmitField, PasswordField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Optional, URL, EqualTo, Email, Length
from app.models import Scenario

class EntryForm(FlaskForm):
    scenario_id = SelectField('Scenario', coerce=int, validators=[DataRequired()], choices=[(0, '-- Select Scenario --')])
    score = IntegerField('Score', validators=[DataRequired(), NumberRange(min=0)])
    proof = StringField('Proof (link to video)', validators=[Optional(), URL()])
    submit = SubmitField('Submit Score')

    def set_choices(self):
        from app.models import Scenario
        choices = [(0, '-- Select Scenario --')] + [(s.id, s.name) for s in Scenario.query.order_by(Scenario.name).all()]
        self.scenario_id.choices = choices

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

class ScenarioForm(FlaskForm):
    name = StringField('Scenario Name', validators=[DataRequired(), Length(max=100)])
    notes = StringField('Notes')

    # Multi-select
    tags = SelectMultipleField('Tags', choices=[
        ('Abilities', 'Abilities'),
        ('Clicking', 'Clicking'),
        ('Flicking', 'Flicking'),
        ('Tracking', 'Tracking'),
        ('Flying', 'Flying'),
        ('Speed', 'Speed')
    ])

    difficulty = SelectField('Difficulty', choices=[
        ('★☆☆☆☆', '★☆☆☆☆'),
        ('★★☆☆☆', '★★☆☆☆'),
        ('★★★☆☆', '★★★☆☆'),
        ('★★★★☆', '★★★★☆'),
        ('★★★★★', '★★★★★')
    ])

    hero = SelectField('Hero', coerce=int, validators=[DataRequired()])

    target = SelectField('Target', coerce=int, validators=[DataRequired()])

    scoring = SelectField('Scoring', choices=[
        ('Kills', 'Kills'),
        ('Total Score', 'Total Score')
    ])

    target_type = SelectField('Target Type', choices=[
        ('Fixed', 'Fixed'),
        ('Random', 'Random')
    ])

    target_distance = SelectField('Target Distance', choices=[
        ('', '-- None --'),
        ('10', '10'), ('20', '20'), ('30', '30'), ('40', '40'), ('50', '50'), ('60', '60')
    ], validators=[Optional()])

    target_range = SelectField('Target Range', choices=[
        ('Short-Range', 'Short-Range'),
        ('Mid-Range', 'Mid-Range'),
        ('Long-Range', 'Long-Range')
    ])

    movement_type = SelectField('Movement Type', choices=[
        ('Static', 'Static'),
        ('Dynamic', 'Dynamic')
    ])

    movement_action = SelectField('Movement Action', choices=[
        ('Horizontal', 'Horizontal'),
        ('Vertical', 'Vertical'),
        ('Random', 'Random')
    ])

    movement_speed = SelectField('Movement Speed', choices=[
        ('Normal', 'Normal'),
        ('Quick', 'Quick'),
        ('Super-Fast', 'Super-Fast')
    ])

    timer = SelectField('Timer (seconds)', choices=[
        ('60', '60'),
        ('120', '120')
    ], coerce=int)

    stay_behind_line = SelectField('Stay Behind Line', choices=[
        ('Yes', 'Yes'),
        ('No', 'No')
    ])

    use_abilities = SelectField('Use Abilities', choices=[
        ('Yes', 'Yes'),
        ('No', 'No')
    ])

    no_ability_cooldown = SelectField('No Ability Cooldown', choices=[
        ('True', 'True'),
        ('False', 'False')
    ])

    submit = SubmitField('Submit Scenario')

    # New method to set dynamic choices for hero and target from the Character table.
    def set_dynamic_choices(self):
        from app.models import Character
        characters = Character.query.order_by(Character.name).all()
        self.hero.choices = [(c.id, c.name) for c in characters]
        self.target.choices = [(c.id, c.name) for c in characters]