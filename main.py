import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from configs.config import Development, Production

app = Flask(__name__)

# configs
app.config.from_object(Development)

conn = psycopg2.connect("dbname='Techome' user='postgres' host='localhost' password='12121994'")
# conn = psycopg2.connect("dbname='d36lve8t356t1v' user='blufcyfuephvbf' host='ec2-176-34-184-174.eu-west-1.compute.amazonaws.com' password='f6bb9cce21036c899c21ea893eb19ef5568e2ef2c22316547c6ee5f3f149206a'")

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

from routes import *