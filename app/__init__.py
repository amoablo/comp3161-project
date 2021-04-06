from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import psycopg2
# import MYSQLdb
import mysql.connector as mysql


import os

app = Flask(__name__)

app.config['SECRET_KEY'] = "GqAExVdKcc66GNtuceYYSUSkJ3bhsULZhQZtT2xDrrAtz6KG4M6Xm"

# Setup database connection

hostname = 'localhost'
username = 'comp3161-project2'
password = 'comp3161-project2'
database = 'comp3161_project2_mealplanner'

# Connect to mysql database
db = mysql.connect(host= hostname, 
                database= database,
                user= username,
                password= password)   

# Connect to postgress databse
# db = psycopg2.connect(host= hostname, 
#                 database= database,
#                 user= username,
#                 password= password) 


app.config.from_object(__name__)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views