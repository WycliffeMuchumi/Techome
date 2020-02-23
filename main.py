import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, redirect, flash, request, abort
from forms import SignUpForm, LoginForm, UpdateSignUpForm, PostForm, RequestResetForm, PasswordResetForm
from flask_sqlalchemy import SQLAlchemy
from configs.config import Development, Production
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
import psycopg2

app = Flask(__name__)

# configs
app.config.from_object(Production)
# app.config['WHOOSH_BASE'] = 'whoosh'

# conn = psycopg2.connect("dbname='Techome' user='postgres' host='localhost' password='12121994'")
conn = psycopg2.connect("dbname='d36lve8t356t1v' user='blufcyfuephvbf' host='ec2-176-34-184-174.eu-west-1.compute.amazonaws.com' password='f6bb9cce21036c899c21ea893eb19ef5568e2ef2c22316547c6ee5f3f149206a'")



# SQLAlchemy instance
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# Setting up our mail server
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# using environment variable to set up our username and password attributes(use of os module)
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
# Initializing our flask_mail extension
mail = Mail(app)
from models import User, Post


@app.before_first_request
def create_table():
    db.create_all()
    # db.drop_all()


@app.route('/')
@app.route('/home')
def home():
    # Displaying all the other pages using pagination
    page = request.args.get('page', 1, type=int)
    # Using pagination to display 5 posts per page
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


# This is a sign up route that enables users to create accounts

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # here we are instantiating a user and passing in the user's attributes to capture the data passed in by a new user during signup
        user = User(first_name=form.first_name.data, second_name=form.second_name.data, username=form.username.data,
                    email=form.email.data, password=hashed_password)
        # adds this user to the changes we want to do in our database
        db.session.add(user)
        # adds the user to the database
        db.session.commit()
        flash('Your account has been created successfully,You can now login to your account!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='SignUp', form=form)


# This is a login route that enables users to login to their accounts

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # session['email'] = form.email.data
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful.Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# @app.route('/events', methods=['GET', 'POST'])
# def events():
#     return render_template('events.html', title='Events')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateSignUpForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        # saving the data if it is valid on submit
        db.session.commit()
        flash('Your Profile has been updated successfully', 'success')
        return redirect(url_for('account'))
    # populating the form with the details of the current user
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.second_name.data = current_user.second_name
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pictures/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


# using random hex to randomise picture name since we dont need the name of the picture users upload to
# avoid conflicts with existing similar picture names in our profile pictures folder
# using os module to ensure the form captures the file extension of the image as uploaded by the user
def save_profile_picture(user_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(user_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pictures', picture_filename)
    # resizing the picture uploaded by the user before it is saved
    output_size = (215, 125)
    new_image = Image.open(user_picture)
    new_image.thumbnail(output_size)
    new_image.save(picture_path)
    return picture_filename


# The below route allows a user to create a new post
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, post_content=form.post_content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post has been created successfully', 'success')
        return redirect(url_for('home'))

    return render_template('create_post.html', title='New-Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    # The below code means that the function should return a post with the passed id or else throw a 404 error
    post = Post.query.get_or_404(post_id)
    return render_template('get_post.html', title='post.title', post=post)


# The below route enables the current_user to edit the post he or she created

@app.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Below line of code ensures that only the author of the post can edit it
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        form.title.data = post.title
        form.post_content.data = post.post_content
        db.session.commit()
        flash('Your Post Has Been Updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.post_content.data = post.post_content
    return render_template('create_post.html', title='Edit-Post', form=form, legend='Edit Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


# The below route shows all the posts created by a specific author
@app.route('/user/<string:username>')
def user_posts(username):
    # Displaying all the other pages using pagination
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # Using pagination to display 5 posts per page
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('posts_by_user.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    # The _external = True will give us an obsolete url instead of a relative url
    msg.body = f'''To reset your password, click on the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request kindly ignore this email notification and no changes will be made'''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with steps to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


# The below route enables sending of an URL link containing a token to the user to reset password
@app.route('/reset_request/<token>')
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That token is invalid or expired', 'warning')
        return redirect(url_for('reset_request'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        # commiting changes made to the user's password
        db.session.commit()
        flash('Your password has been reset successfully,You can now login to your account!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


# @app.route('/search')
# def search():
#     posts = Post.query.whoosh_search(request.args.get('query')).all()
#     return render_template('home.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)
