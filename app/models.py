from flask_login import UserMixin

# class User(UserMixin):
#     # Using UserMixin instead of db.Model

#     def __init__(self, user_id, first_name, last_name, email, gender, password):
#         self.user_id = user_id
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email = email
#         self.gender = gender
#         self.password = password

#     def is_authenticated(self):
#         return True

#     def is_active(self):
#         return True

#     def is_anonymous(self):
#         return False

#     def get_id(self):
#         try:
#             return unicode(self.user_id)  # python 2 support
#         except NameError:
#             return str(self.user_id)  # python 3 support

#     def __repr__(self):
#         return '<User %r>' % (self.email)
from . import db
from .databasemanager import *
from datetime import datetime

# from databasemanager import * # for testing only


# create the objects to communicate with database

class User(UserMixin): 
    def __init__(self, id=None, fname="test",lname="test", email="test@test,com", gender="O", password="1234"):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.gender = gender
        self.password = password
        self.recipes = []
        self.ingredients = []
        self.mealPlans = []
    
    def validateUser(self, password):
        return password == self.password
    
    def setRecipes(self):
        self.recipes = getUserRecipes(self.id)
    
    def setIngredients(self):
        self.ingredients = getUserIngredient(self.id)

    def setMealPlans(self):
        self.mealPlans = getUserMealPlans(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.email)

class Recipe:
    def __init__(self, id=None, name="test", date_created=datetime.now(), calorie=1000, image_url="recipe/test.png"):
        self.id = id
        self.name = name
        self.date_created = date_created
        self.calorie = calorie
        self.image_url = image_url
        self.instructions = []
        self.ingredients = []
    
    def setIngredients(self):
        self.ingredients = getAllIngredients(self.id)

    def setInstructions(self):
        self.instructions = getAllInstructions(self.id)

class Ingredient:
    def __init__(self, id=None, name="test", unit="count", quantity=0):
        self.id = id
        self.name = name
        self.unit = unit
        self.quantity = quantity

class Instruction:
    def __init__(self, id=None, step_no=-1, description="Start the fire"):
        self.id = id
        self.step_no = step_no
        self.description = description

class Meal:
    def __init__(self, id=None, num_serving=1, recipe_id=1):
        self.id = id
        self.num_serving = num_serving
        self.recipe_id = recipe_id
        self.calorie = 0
        self.recipe = None
    
    def setRecipe(self):
        self.recipe = getRecipe(self.recipe_id)

class MealPlan:
    def __init__(self, id=None, date=datetime.now(), week_num=1):
        self.id = id
        self.date = date
        self.week_num = week_num
        self.lunch_id = None
        self.dinner_id = None
        self.breakfast_id = None
        self.meals = []

    def getMeals(self):
        self.meals, (self.lunch_id, self.dinner_id, self.breakfast_id) = getMealPlanMeals(self.id)
