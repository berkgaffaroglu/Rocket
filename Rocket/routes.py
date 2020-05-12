from flask import render_template, url_for, flash, redirect,request
from Rocket import app,db,bcrypt
from Rocket.forms import RegistrationForm, LoginForm 
from Rocket.models import User, Todo
from flask_login import login_user,logout_user,current_user, login_required
#Setting up routes 
@app.route('/') 
@app.route('/index') 
@app.route('/home') 
def home(): 
    return render_template('index.html', title="Home") 
 
@app.route('/login', methods=['GET','POST']) 
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))

            
        else:
            flash(f'Login was unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html', title="Login", form=form) 
 
@app.route('/signup', methods=['GET','POST']) 
def signup(): 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_pw, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for: {form.username.data}', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Sign Up", form=form) 
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
        return render_template('account.html', title="Account") 