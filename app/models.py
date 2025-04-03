from datetime import datetime
from app import db
from flask_login import UserMixin

# -----------------------------
# User Model
# -----------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    entries = db.relationship('Entry', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

# -----------------------------
# Scenario Model
# -----------------------------
class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100))
    notes = db.Column(db.Text)
    tags = db.Column(db.String(200))
    difficulty = db.Column(db.String(10))
    hero = db.Column(db.String(50))
    target = db.Column(db.String(50))
    scoring = db.Column(db.String(50))
    target_type = db.Column(db.String(50))
    target_distance = db.Column(db.String(50))
    target_range = db.Column(db.String(50))
    movement_type = db.Column(db.String(50))
    movement_action = db.Column(db.String(50))
    movement_speed = db.Column(db.String(50))
    timer = db.Column(db.Integer)
    stay_behind_line = db.Column(db.String(10))
    use_abilities = db.Column(db.String(10))
    no_ability_cooldown = db.Column(db.String(10))
    scenario_code = db.Column(db.String(20), unique=True)

    entries = db.relationship('Entry', backref='scenario', lazy='dynamic')

    def __repr__(self):
        return f'<Scenario {self.name}>'

# -----------------------------
# Entry Model (Score Logs)
# -----------------------------
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'))
    score = db.Column(db.Integer, nullable=False)
    proof = db.Column(db.String(500))  # Optional link to a video
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Entry {self.score} for Scenario {self.scenario_id}>'
    
# -----------------------------
# Flask-Login Directions (Temporary)
# -----------------------------
from app import login

@login.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))