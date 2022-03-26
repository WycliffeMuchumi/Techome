from main import db, login_manager, app
from flask_login import UserMixin, current_user
from datetime import datetime
from wtforms.validators import ValidationError
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# The below decorator reloads user from the user_id stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# This is a user model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    second_name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    # user_id is the payload that we will pass to the token below
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        # creating our token
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # The below static method verifies our token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # specifies the way we want our objects to be printed out
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

    # The below method validates the user input username  to avoid duplication of username in the database

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken,please choose a different one')

    # The below method validates the user input email to avoid duplication of emails in the database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken,please choose a different one')

    # This method updates the username if the data been input is not the same as in the database
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken,please choose a different one')

    # This method updates the email if the data been input is not the same as in the database
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken,please choose a different one')

    # The below method checks if the user by the specified email exists in the database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Account Does Not Exist,Register First', 'danger')


# This is a post model
class Post(db.Model):
    __tablename__ = 'posts'
    # __searchable__ = ['username', 'title', 'content']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


def __repr__(self):
    return f"Post('{self.title}','{self.date_posted}')"


