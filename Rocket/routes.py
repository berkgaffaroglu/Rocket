from flask import render_template, url_for, flash, redirect 
from Rocket import app,db,bcrypt
from Rocket.forms import RegistrationForm, LoginForm 
from Rocket.models import User, Todo
 
#Setting up routes 
@app.route('/') 
@app.route('/index') 
@app.route('/home') 
def home(): 
    return render_template('index.html', title="Home") 
 
@app.route('/login', methods=['GET','POST']) 
def login(): 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            bcrypt.check_password_hash(user.password, form.password.data)
            flash(f'You are logged in: { user.username }', 'success')

    return render_template('login.html', title="Login", form=form) 
 
@app.route('/signup', methods=['GET','POST']) 
def signup(): 
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_pw, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for: {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Sign Up", form=form) 
