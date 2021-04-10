from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField
from wtforms.validators import InputRequired, DataRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    
class SignUpForm(FlaskForm):
    firstname=StringField('Firstname', validators=[InputRequired()])
    lastname=StringField('Lastname', validators=[InputRequired()])
    email = StringField("Email",  validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    
class MealPlanForm(FlaskForm):
    calories = IntegerField("Calories", validators=[DataRequired()], description="Number of calories\
         for the week")

class RecipeForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    calories = IntegerField("Calories", validators=[DataRequired()], description="Number of calories for the meal that will be created from this recipe")
    ingredients = TextAreaField("Ingredient", validators=[DataRequired()], description="Number of steps for to prepare a meal from this recipe")
    # no_ingredients = IntegerField("No. of Ingredients", validators=[DataRequired()], description="")
    # no_instructions = IntegerField("No. of Instructions", validators=[DataRequired()], description="")
    instructions = TextAreaField('Instruction', validators=[DataRequired()])
    image = FileField('Image of Meal', validators=[
        FileRequired(),
        FileAllowed(['jpg','png','jpeg'], 'Images only')
    ])

class rsearchForm(FlaskForm):
    rname=StringField('Recipe_Name', 
                        validators=[InputRequired()], 
                        description="Enter recipe name")
                        
