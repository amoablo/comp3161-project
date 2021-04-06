from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired, DataRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    
class SignUpForm(FlaskForm):
    firstname=StringField('Firstname', validators=[DataRequired()])
    lastname=StringField('Lastname', validators=[DataRequired()])
    gender=StringField('gender', validators=[InputRequired()])
    email = StringField("Email",  validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])