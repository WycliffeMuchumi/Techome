import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from configs.config import Production

app = Flask(__name__)

# configs
app.config.from_object(Production)

#conn = psycopg2.connect("dbname='Techome' user='postgres' host='localhost' password='12121994'")
conn = psycopg2.connect("dbname='dep8r0o8d5cdmg' user='vegyyixqcaeopk' host='ec2-52-48-159-67.eu-west-1.compute.amazonaws.com' password='558ba3166ccfc3fbb08244a69f9c10289840ece23e12199106abee3e9a5f50d2'")

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

from app.views import *