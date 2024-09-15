from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, RegistrationForm, PlanTrainingForm
from flask_login import current_user, login_user
import sqlalchemy as sa
from app import db
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from urllib.parse import urlsplit
from datetime import datetime, timezone, timedelta
from app.forms import EditProfileForm
from app.forms import EmptyForm
from app.forms import PostForm
from app.models import User, Post, Calendar, PlannedTraining
import sqlalchemy as sa

# Diese Funktion wird vor jeder Anfrage aufgerufen und aktualisiert das 'last_seen'-Feld des Benutzers
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

# Route für die Startseite und das Dashboard
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required  # Login erforderlich
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user, activity_type=form.activity_type.data, duration=form.duration.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = db.paginate(current_user.following_posts(), page=page,
                        per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

# Route für die "Explore"-Seite
@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page,
                        per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('explore.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

# Route für das Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# Route für das Logout
@app.route('/logout')
def logout():
    logout_user()  # Beendet die Benutzersitzung
    return redirect(url_for('index'))

# Route für die Registrierung neuer Benutzer
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Route für Benutzerprofile
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)

# Route zum Bearbeiten des Benutzerprofils
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

# Route zum Folgen eines Benutzers
@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

# Route zum Entfolgen eines Benutzers
@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

# Import der nötigen Module für den Kalender
from flask import render_template, redirect, url_for, request
from .models import Calendar
from .forms import CalendarForm
from . import db
from flask_login import current_user

# Route für den Kalender
@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    form = PlanTrainingForm()
    if form.validate_on_submit():
        planned_training = PlannedTraining(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            time=form.time.data,
            activity_type=form.activity_type.data
        )
        db.session.add(planned_training)
        db.session.commit()
        flash('Your training has been planned!')
        return redirect(url_for('calendar'))

    # Kalender für den aktuellen Monat erstellen
    today = datetime.today()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    calendar_days = []
    current_day = start_of_month
    while current_day <= end_of_month:
        calendar_days.append(current_day)
        current_day += timedelta(days=1)

    planned_trainings = PlannedTraining.query.filter_by(user_id=current_user.id).all()

    return render_template('calendar.html', form=form, calendar_days=calendar_days, today=today, planned_trainings=planned_trainings)

# Route zum Erstellen eines neuen Kalendereintrags
@app.route('/calendar/new', methods=['GET', 'POST'])
@login_required
def new_calendar():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user, activity_type=form.activity_type.data, duration=form.duration.data)
        db.session.add(post)
        db.session.commit()
        flash('Your calendar entry is now live!')
        return redirect(url_for('calendar'))
    return render_template('new_calendar.html', form=form)

# Route für das Dashboard, das eine Übersicht der Trainingseinheiten anzeigt
@app.route('/dashboard')
@login_required
def dashboard():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    total_minutes = sum(post.duration for post in posts)
    activity_breakdown = {
        'Laufen': sum(post.duration for post in posts if post.activity_type == 'Laufen'),
        'Krafttraining': sum(post.duration for post in posts if post.activity_type == 'Krafttraining'),
        'Fahrradfahren': sum(post.duration for post in posts if post.activity_type == 'Fahrradfahren')
    }
    return render_template('dashboard.html', total_minutes=total_minutes, activity_breakdown=activity_breakdown)
