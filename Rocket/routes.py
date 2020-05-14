import os
from PIL import Image
import secrets
from flask import render_template, url_for, flash, redirect,request,abort
from Rocket import app,db,bcrypt
from Rocket.forms import RegistrationForm, LoginForm,UpdateProfileForm,CreatePostForm
from Rocket.models import User, Post
from flask_login import login_user,logout_user,current_user, login_required
#Setting up routes 
@app.route('/') 
@app.route('/index') 
@app.route('/home') 
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_post.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', posts=posts)
 
@app.route('/login', methods=['GET','POST']) 
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for('home'))
        else:
            user = User.query.filter_by(username=form.email.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            old_picture = current_user.image_file
            old_picture_path = os.path.join(app.root_path, 'static/profile_pics', old_picture)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            if old_picture != 'default.jpg':
                os.remove(old_picture_path)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form) 
@login_required
@app.route('/createpost',methods=['GET','POST'])
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('home'))
    return render_template('create_post.html', legend="Create New Post", title="Create New Post", form=form)


@app.route('/post/<int:post_id>', methods=['GET','POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = CreatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', legend='Update Post', form=form)



@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_post.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

