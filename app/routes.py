# Standard Library
from datetime import datetime

# Third-Party Libraries
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

# Local Imports
from app import db
from app.models import Scenario, Entry, User
from app.forms import EntryForm, RegistrationForm, LoginForm


bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    return '<h1>MRAT is alive!</h1>'


@bp.route('/scenarios')
def scenario_list():
    scenarios = Scenario.query.all()
    return render_template('scenarios.html', scenarios=scenarios)


@bp.route('/entries')
def entry_list():
    entries = Entry.query.order_by(Entry.timestamp.desc()).all()
    return render_template('entries.html', entries=entries)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Logged in successfully.', 'success')
            return redirect(next_page or url_for('main.home'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))


@bp.route('/my-entries')
@login_required
def my_entries():
    entries = Entry.query.filter_by(user_id=current_user.id)\
                         .order_by(Entry.timestamp.desc()).all()
    return render_template('my_entries.html', entries=entries)


@bp.route('/play', methods=['GET', 'POST'])
@login_required
def play():
    form = EntryForm()
    form.set_choices()

    # Get scenario_id from query string
    scenario_id = request.args.get('scenario_id', type=int)
    selected_scenario = Scenario.query.get(scenario_id) if scenario_id else None

    if form.validate_on_submit():
        entry = Entry(
            user_id=current_user.id,
            scenario_id=form.scenario_id.data,
            score=form.score.data,
            proof=form.proof.data
        )
        db.session.add(entry)
        db.session.commit()
        flash('Score logged successfully!', 'success')
        return redirect(url_for('main.play', scenario_id=form.scenario_id.data))

    return render_template('play.html', form=form, scenario=selected_scenario)


@bp.route('/leaderboard')
def leaderboard():
    from app.forms import EntryForm  # reuse scenario dropdown logic
    form = EntryForm()
    form.set_choices()

    scenario_id = request.args.get('scenario_id', type=int)
    selected_scenario = Scenario.query.get(scenario_id) if scenario_id else None

    entries = []
    if selected_scenario:
        entries = Entry.query.filter_by(scenario_id=selected_scenario.id)\
                             .order_by(Entry.score.desc()).limit(10).all()

    return render_template('leaderboard.html',
                           form=form,
                           scenario=selected_scenario,
                           entries=entries)