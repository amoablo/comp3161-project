from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired, DataRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    
class SignUpForm(FlaskForm):
    firstname=StringField('Firstname', validators=[InputRequired()])
    lastname=StringField('Lastname', validators=[InputRequired()])
    gender=StringField('gender', validators=[InputRequired()])
    email = StringField("Email",  validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    
class MealPlanForm(FlaskForm):
    calories = IntegerField("Calories", validators=[DataRequired()], description="Number of calories\
         for the week")

class RecipForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    calories = IntegerField("Calories", validators=[DataRequired()], description="Number of calories for the meal that will be created from this recipe")
    number_of_steps = IntegerField("No. of Steps", validators=[DataRequired()], description="Number of steps for to prepare a meal from this recipe")
    step_description = TextAreaField('Description of Steps', validators=[DataRequired()])