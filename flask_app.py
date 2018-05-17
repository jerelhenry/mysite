
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View
from flask_sslify import SSLify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask import redirect
from flask import url_for
from wtforms.validators import ValidationError
from flask import flash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user


app = Flask(__name__)

app.config.from_object('config.BaseConfig')
db = SQLAlchemy(app)
login = LoginManager(app)
Bootstrap(app)
SSLify(app)
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.Integer)
    name = db.Column(db.String(80))
    teacher_name = db.Column(db.String(80))
    resource_name = db.Column(db.String(80))
    resource_url = db.Column(db.String(300))

class Song(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(80))
     artist_name = db.Column(db.String(80))
     youtube_url = db.Column(db.String(300))

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField(
        'Email', validators=[InputRequired(), Email()])
    password = PasswordField(
        'Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Register')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please choose a different username.')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15))
    email = db.Column(db.String(150))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Sign in')

@login.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/about_me')
def about_me():
    return render_template('about_me.html')

@app.route('/class_schedule')
def class_schedule():
    courses = Course.query.all()
    return render_template('class_schedule.html',
                           courses=courses)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('homepage'))
    return render_template('registration.html', form=form)

@app.route('/top_ten_songs')
def top_ten_songs():
    songs = Song.query.all()
    return render_template('top_ten_songs.html', songs=songs)

if __name__ == '__main__':
  db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Username or password is incorrect.', 'danger')
            return render_template('login.html', form=form)
        login_user(user)
        return redirect(url_for('homepage'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

nav = Nav(app)
@nav.navigation('mysite_navbar')
def create_navbar():
    home_view = View('Home', 'homepage')
    login_view = View('Login', 'login')
    logout_view = View('Logout', 'logout')
    registration_view = View('Registration', 'registration')
    about_me_view = View('About Me', 'about_me')
    class_schedule_view = View('Class Schedule', 'class_schedule')
    top_ten_songs_view = View('Top Ten Songs', 'top_ten_songs')
    misc_subgroup = Subgroup('Misc',
                             about_me_view,
                             class_schedule_view,
                             top_ten_songs_view)
    if current_user.is_authenticated:
        return Navbar('MySite', home_view, misc_subgroup, logout_view)
    else:
        return Navbar('MySite', home_view, misc_subgroup, login_view, registration_view)