from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = "GqAExVdKcc66GNtuceYYSUSkJ3bhsULZhQZtT2xDrrAtz6KG4M6Xm"

# Setup SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = ""
app.config['DATABASE_HOST'] = os.environ.get('DATABASE_HOST')
app.config['DATABASE_USER'] = os.environ.get('DATABASE_USER')
app.config['DATABASE_PASSWORD'] = os.environ.get('DATABASE_PASSWORD')
app.config['DATABASE_NAME'] = os.environ.get('DATABASE_NAME')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = './uploads'
db = SQLAlchemy(app)

app.config.from_object(__name__)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views