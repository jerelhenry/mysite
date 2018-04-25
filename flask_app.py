
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import render_template
import constants

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/about_me')
def about_me():
    return render_template('about_me.html')

@app.route('/class_schedule')
def class_schedule():
    return render_template('class_schedule.html',
                           courses=constants.COURSES)

@app.route('/registration')
def registration():
    return render_template('registration.html')

