from flask import render_template, url_for, flash, redirect 
from Rocket import app 
from Rocket.forms import RegistrationForm, LoginForm 
from Rocket.models import User, Post 
 
#Setting up routes 
@app.route('/') 
@app.route('/index') 
@app.route('/home') 
def home(): 
    return render_template('index.html', title="Home") 
 
@app.route('/login') 
def login(): 
    return render_template('login.html', title="Login") 
 
@app.route('/register') 
def register(): 
    return render_template('register.html', title="Register") 
