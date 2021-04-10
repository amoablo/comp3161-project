from app import app, db, connectdb
import mysql.connector as mysql
from datetime import datetime

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
        self.shoppingList = []
    
    def validateUser(self, password):
        return password == self.password
    
    def setRecipes(self):
        self.recipes = getUserRecipes(self.id)
    
    def setIngredients(self):
        self.ingredients = getUserIngredient(self.id)

    def setMealPlans(self):
        self.mealPlans = getUserMealPlans(self.id)
    
    def setShoppingList(self):
        self.setIngredients()
        self.setMealPlans()
        mealplanMeals = []
        mp_ingredients = []
        mp_ingredients_no_dup = []

        # get all the meals for the mealplans
        for mealPlan in self.mealPlans:
            mealPlan.setMeals()
            mealplanMeals += mealPlan.meals

        # get all recipes for the meals
        for meal in mealplanMeals:
            meal.setRecipe()
            mp_ingredients += meal.ingredients 

        # remove duplicates
        for ingr in mp_ingredients:
            cpy_ingredients = []
            cpy_ingredients += mp_ingredients

            ingr_indx = mp_ingredients.index(ingr)

            for indx in range(ingr_indx+1, len(cpy_ingredients)):
                if(ingr.id == cpy_ingredients[indx].id):
                    ingr.quantity += cpy_ingredients[indx].quantity
                    mp_ingredients.remove(cpy_ingredients[indx])

            mp_ingredients_no_dup.append(ingr)
        
        # remove ingredients that are already in the store
        self.setIngredients()

        for indx in range(len(mp_ingredients_no_dup)):
            for ingr_store in self.ingredients:
                if mp_ingredients_no_dup[indx].id == ingr_store.id:
                    mp_ingredients_no_dup[indx].quantity -= ingr_store.quantity
                    break;
            if mp_ingredients_no_dup[indx].quantity > 0:
                self.shoppingList.append( mp_ingredients_no_dup[indx])

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
        self.ingredients = []
    
    def setRecipe(self):
        self.recipe = getRecipe(self.recipe_id)
        self.recipe.setIngredients()
        self.recipe.setInstructions()
        ingredients = self.recipe.ingredients
        for ingredient in ingredients:
            ingredient.quantity *= self.num_serving
            self.ingredients.append(ingredient)

class MealPlan:
    def __init__(self, id=None, date=datetime.now(), week_num=1):
        self.id = id
        self.date = date
        self.week_num = week_num
        self.lunch_id = None
        self.dinner_id = None
        self.breakfast_id = None
        self.meals = []

    def setMeals(self):
        self.meals, (self.lunch_id, self.dinner_id, self.breakfast_id) = getMealPlanMeals(self.id)


# Database Manager


# Code for testing

# # ---------------------------------------------

# from models import *


# # Setup database connection

# hostname = 'localhost'
# username = 'comp3161-project2'
# password = 'comp3161-project2'
# database = 'comp3161-project2'

# # Connect to mysql database
# db = mysql.connect(host= hostname, 
#                 database= database,
#                 user= username,
#                 password= password)  

# # ---------------------------------------

# setup the database cursor 



# users database request 

def getAllUser(): # return a list of users
    cursor = db.cursor()

    command = "select * from users;"
    cursor.execute(command)
    # cursor.commit()
    response = cursor.fetchall()

    users = []

    if len(response) > 0 :     
        for user_data in response:
            users.append(User(
                user_data[0], 
                user_data[1], 
                user_data[2], 
                user_data[3], 
                user_data[4], 
                user_data[5] ))

    return users

def getUser(id):
    cursor = db.cursor()

    command = "select * from users where user_id = {};".format(
        id
    )
    cursor.execute(command)
    response = cursor.fetchall()

    fetchUser = None

    if len(response) > 0 :        
        fetchUser = User(response[0][0], 
                        response[0][1], 
                        response[0][2], 
                        response[0][3], 
                        response[0][4], 
                        response[0][5] )
   
    return fetchUser

def addUser(user):
    cursor = db.cursor()

    command = "insert into users (first_name, last_name, email, gender, password) values ( %s, %s, %s, %s, %s);"

    cursor.execute(command,(
        user.fname,
        user.lname,
        user.email,
        user.gender,
        user.password
    ))
    db.commit()

def updateUser(user):
    cursor = db.cursor()

    command = "update users set first_name=%s, last_name=%s, email=%s, gender=%s, password=%s where user_id=%s;"
    cursor.execute(command,(
        user.fname,
        user.lname,
        user.email,
        user.gender,
        user.password,
        user.id
    ))
    db.commit()

def removeUser(id):
    cursor = db.cursor()

    command = "delete from users where user_id={}".format(id)
    cursor.execute(command)
     

# recipe database request 

def getAllRecipes():
    cursor = db.cursor()

    command = "select * from recipe;"
    cursor.execute(command)
    response = cursor.fetchall()

    recipes = []

    if len(response) > 0 :     
        for data in response:
            recipes.append(Recipe(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4]
            ))

    return recipes

def getRecipe(id):
    cursor = db.cursor()

    command = "select * from recipe where recipe_id = {};".format(
        id
    )
    cursor.execute(command)
    response = cursor.fetchall()

    fetchRecipe = None

    if len(response) > 0 :        
        fetchRecipe = Recipe(response[0][0], 
                        response[0][1], 
                        response[0][2], 
                        response[0][3], 
                        response[0][4] )
   
    return fetchRecipe

def getRecipes(name):
    cursor = db.cursor()

    command = """select * from recipe where name LIKE "%{}%"; """.format(
        name
    )
    cursor.execute(command)
    response = cursor.fetchall()

    recipes = []

    if len(response) > 0 :     
        for data in response:
            recipes.append(Recipe(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4]
            ))

    return recipes

def addNewRecipe(user_id, recipe):
    cursor = db.cursor()

    command = "insert into recipe (name, created_date, calorie, image_url) values (%s, %s, %s, %s);"

    cursor.execute(command,(
        recipe.name,
        recipe.date_created,
        recipe.calorie,
        recipe.image_url,
    ))
    db.commit()

def updateRecipe(recipe):
    cursor = db.cursor()

    command = "update recipe set name=%s, created_date=%s, calorie=%s, image_url=%s where recipe_id=%s;"
    cursor.execute(command,(
        recipe.name,
        recipe.date_created,
        recipe.calorie,
        recipe.image_url,
        recipe.id
    ))
    db.commit()

def removeRecipe(id):
    cursor = db.cursor()

    command = "delete from recipe where recipe_id={}".format(id)
    cursor.execute(command)
    db.commit()


# ingredient database request 

def getAllIngredients(recipe_id):
    dbb = connectdb()
    cursor = dbb.cursor()

    command = """
    call getingredients(%s);
    """

    cursor.execute(command,(recipe_id,))
    response = cursor.fetchall()
    dbb.close()

    ingredients = []

    if len(response) > 0 :     
        for data in response:
            ingredients.append(Ingredient(
                data[0],
                data[1],
                data[2],
                data[3]
            ))

    return ingredients

def getIngredient(id):
    dbb = connectdb() 
    cursor = dbb.cursor()

    command = """
    call getingredient(%s);
    """
    cursor.execute(command, (id,))
    response = cursor.fetchall()
    dbb.close()


    fetchIngred = None

    if len(response) > 0 :        
        fetchIngred = Ingredient(id = response[0][0], 
                        name = response[0][1], 
                        unit  = response[0][2] )
   
    return fetchIngred

def getIngredientByName(name):
    dbb = connectdb() 
    cursor = dbb.cursor()

    command = """
    SELECT ingred.ingredient_id, ingred.name, ingr_unit.unit
    FROM ((Select * from ingredients
        WHERE ingredients.name = %s) ingred

    LEFT JOIN (SELECT measured_in.ingredient_id , measurement.unit
                FROM measured_in
                LEFT JOIN measurement
                on measured_in.measurement_id = measurement.measurement_id)as ingr_unit
    on ingred.ingredient_id = ingr_unit.ingredient_id);
    """
    cursor.execute(command, (name,))
    response = cursor.fetchall()
    dbb.close()


    fetchIngred = None

    if len(response) > 0 :        
        fetchIngred = Ingredient(id = response[0][0], 
                        name = response[0][1], 
                        unit  = response[0][2] )
   
    return fetchIngred

def addIngredient(recipe_id, n_ingredient):
    cursor = db.cursor()

    command_ingr = "insert into ingredients (name) values (%s);"
    command_get_ingr_id = "SELECT `AUTO_INCREMENT` FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ingredients';"
    command_made_of = "insert into made_of (recipe_id, ingredient_id, amount) values ( %s, %s, %s);"
    command_getmeasurementid = "SELECT measurement.measurement_id from measurement WHERE measurement.unit= '{}';".format(n_ingredient.unit)
    command_measur = "insert into measured_in (ingredient_id, measurement_id) values ( %s, %s);"

    # get increment value
    cursor.execute(command_get_ingr_id)
    response = cursor.fetchall()
    n_ingredient_id = response[0][0]
    
    # insert ingredient
    cursor.execute(command_ingr,(
        n_ingredient.name,
    ))
    
    db.commit()


    # insert made of
    cursor.execute(command_made_of,(
        recipe_id,
        n_ingredient_id,
        n_ingredient.quantity,
    ))

    db.commit()

    #get measurement id and insert measured in
    cursor.execute(command_getmeasurementid)
    response = cursor.fetchall()
    measurement_id = response[0][0]

    cursor.execute(command_measur,(
        n_ingredient_id,
        measurement_id,
    ))

    db.commit()

def updateIngredient(recipe_id, n_ingredient):
    cursor = db.cursor()

    command_getmeasurementid = "SELECT measurement.measurement_id from measurement WHERE measurement.unit= '{}';".format(n_ingredient.unit)
    command_ingr = "update ingredients set name=%s where ingredient_id=%s ;"
    command_made_of = "update made_of set amount=%s where recipe_id=%s and ingredient_id=%s"
    command_measured_in = "update measured_in set measurement_id=%s where ingredient_id=%s"

    # get measuremen id
    cursor.execute(command_getmeasurementid)
    response = cursor.fetchall()
    measurement_id = response[0][0]

    #update ingredient
    cursor.execute(command_ingr,(
        n_ingredient.name,
        n_ingredient.id,
    ))
    db.commit()

    # update made of
    cursor.execute(command_made_of,(
        n_ingredient.quantity,
        recipe_id,
        n_ingredient.id,
    ))
    db.commit()

    # uodate measured in
    cursor.execute(command_measured_in,(
        measurement_id,
        n_ingredient.id,
    ))
    db.commit()

def removeIngredient(id):
    cursor = db.cursor()

    command = "delete from ingredients where ingredient_id={}".format(id)
    cursor.execute(command)
    db.commit()


# instructions database request 

def getAllInstructions(recipe_id):
    cursor = db.cursor()

    command = """
    SELECT * from instructions 
    WHERE instructions.instruction_id in (SELECT prepare.instruction_id FROM prepare
                                        WHERE prepare.recipe_id={}) 
    """.format(recipe_id)

    cursor.execute(command)
    response = cursor.fetchall()

    instructions = []

    if len(response) > 0 :     
        for data in response:
            instructions.append(Instruction(
                data[0],
                data[1],
                data[2],
            ))

    return instructions

def getInstruction(id):
    cursor = db.cursor()

    command = """
    SELECT * from instructions  where instructions.instruction_id = {};
    """.format(id)
    cursor.execute(command)
    response = cursor.fetchall()

    fetchInstruction = None

    if len(response) > 0 :        
        fetchInstruction = Instruction(
                        response[0][0], 
                        response[0][1], 
                        response[0][2] )
   
    return fetchInstruction

def addInstruction(recipe_id, n_instruction):
    cursor = db.cursor()

    command_get_instr_id = "SELECT `AUTO_INCREMENT` FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'instructions';"
    command_prepare = "insert into prepare (recipe_id, instruction_id, step_no) values (%s, %s, %s);"
    command_instructions = "insert into instructions (step_no, step_description) values (%s, %s);"

    # get increment value
    cursor.execute(command_get_instr_id)
    response = cursor.fetchall()
    n_instruction_id = response[0][0]
    
    # insert instruction
    cursor.execute(command_instructions,(
        n_instruction.step_no,
        n_instruction.description,
    ))
    
    db.commit()

    # insert prepare
    cursor.execute(command_prepare,(
        recipe_id,
        n_instruction_id,
        n_instruction.step_no,
    ))

    db.commit()

def updateInstruction( n_instruction):
    cursor = db.cursor()

    command_instructions = "update instructions set step_description=%s where instruction_id=%s ;"
    # command_prepare = "update made_of set amount=%s where recipe_id=%s and ingredient_id=%s"

    #update instruction
    cursor.execute(command_instructions,(
        n_instruction.description,
        n_instruction.id,
    ))
    db.commit()

def removeInstruction(id):
    cursor = db.cursor()

    command = "delete from instructions where instruction_id={}".format(id)
    cursor.execute(command)
    db.commit()


# meal database request 

def getAllMeals():
    cursor = db.cursor()

    command = """
    SELECT meal.meal_id, meal.calorie, meal.num_servings, made_from.recipe_id
    FROM meal
    LEFT JOIN made_from
    ON meal.meal_id = made_from.meal_id;
    """

    cursor.execute(command)
    response = cursor.fetchall()

    meals = []

    if len(response) > 0 :     
        for data in response:
            ml = Meal(
                data[0],
                data[2],
                data[3],
            )
            ml.calorie = data[1]
            meals.append(ml)

    return meals

def getMeal(id):
    cursor = db.cursor()

    command = """
    SELECT ml.meal_id, ml.calorie, ml.num_servings, made_from.recipe_id
    FROM (SELECT * from meal WHERE meal.meal_id={}) ml
    LEFT JOIN made_from
    ON ml.meal_id = made_from.meal_id;
    """.format(id)

    cursor.execute(command)
    response = cursor.fetchall()

    fetchMeal = None

    if len(response) > 0 :        
        fetchMeal = Meal(
                    response[0][0], 
                    response[0][2], 
                    response[0][3] )
     
        fetchMeal.calorie = response[0][1]
   
    return fetchMeal

def addMeal(n_meal):
    cursor = db.cursor()

    command_get_meal_id = "SELECT `AUTO_INCREMENT` FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'meal';"
    command_meal = "insert into meal (calorie, num_servings) values (%s, %s);"
    command_made_from = "insert into made_from (meal_id, recipe_id) values (%s, %s);"

    # get increment value
    cursor.execute(command_get_meal_id)
    response = cursor.fetchall()
    n_meal_id = response[0][0]
    
    # insert meal
    cursor.execute(command_meal,(
        n_meal.calorie,
        n_meal.num_serving,
    ))
    db.commit()

    # insert made_from
    cursor.execute(command_made_from,(
        n_meal_id,
        n_meal.recipe_id,
    ))

    db.commit()

def updateMeal(n_meal):
    cursor = db.cursor()

    command = "update meal set calorie=%s, num_servings=%s where meal_id=%s ;"
    # command_prepare = "update made_of set amount=%s where recipe_id=%s and ingredient_id=%s"

    #update instruction
    cursor.execute(command,(
        n_meal.calorie,
        n_meal.num_serving,
        n_meal.id,
    ))
    db.commit()

def removeMeal(id):
    cursor = db.cursor()

    command = "delete from meal where meal_id={}".format(id)
    cursor.execute(command)
    db.commit()


# mealplan database request 

def getAllMealPlans():
    cursor = db.cursor()

    command = """
    SELECT * from meal_plan ;   
    """

    cursor.execute(command)
    response = cursor.fetchall()

    mealplans = []

    if len(response) > 0 :     
        for data in response:
            mp = MealPlan(
                data[0],
                data[1],
                data[2],
            )
            mealplans.append(mp)

    return mealplans

def getMealPlan(id):
    cursor = db.cursor()

    command = """
    SELECT * from meal_plan where mealplan_id ={};
    """.format(id)

    cursor.execute(command)
    response = cursor.fetchall()

    fetchMealPlan = None

    if len(response) > 0 :        
        fetchMealPlan = MealPlan(
                    response[0][0], 
                    response[0][1], 
                    response[0][2] )
     
   
    return fetchMealPlan

def addMealPlan(n_mealPlan):
    cursor = db.cursor()

    command_get_mealPlan_id = "SELECT `AUTO_INCREMENT` FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'meal_plan';"
    command_mealPlan = "insert into meal_plan (meal_date, week_num) values (%s, %s);"

    # get increment value
    cursor.execute(command_get_mealPlan_id)
    response = cursor.fetchall()
    n_mealplan_id = response[0][0]
    
    # insert mealplan
    cursor.execute(command_mealPlan,(
        n_mealPlan.date,
        n_mealPlan.week_num,
    ))
    db.commit()
    
    # insert breakfast
    if n_mealPlan.breakfast_id is not None:
        command_mp_type = "insert into breakfast (meal_id, mealplan_id) values (%s, %s);"
        cursor.execute(command_mp_type,(
            n_mealPlan.breakfast_id,
            n_mealplan_id,
        ))
    db.commit()

    # insert lunch
    if n_mealPlan.lunch_id is not None:
        command_mp_type = "insert into lunch (meal_id, mealplan_id) values (%s, %s);"
        cursor.execute(command_mp_type,(
            n_mealPlan.lunch_id,
            n_mealplan_id,
        ))
    db.commit()

    # insert dinner
    if n_mealPlan.dinner_id is not None:
        command_mp_type = "insert into dinner (meal_id, mealplan_id) values (%s, %s);"
        cursor.execute(command_mp_type,(
            n_mealPlan.dinner_id,
            n_mealplan_id,
        ))

    db.commit()

def updateMealPlan(n_mealPlan):
    cursor = db.cursor()

    command = "update meal_plan set meal_date=%s, week_num=%s where mealplan_id=%s ;"

    #update instruction
    cursor.execute(command,(
        n_mealPlan.date,
        n_mealPlan.week_num,
        n_mealPlan.id,
    ))
    db.commit()

def removeMealPlan(id):
    cursor = db.cursor()

    command = "delete from meal_plan where mealplan_id={}".format(id)
    cursor.execute(command)
    db.commit()


# Additional Requests

def getUserRecipes(user_id):
    cursor = db.cursor()

    command = """
    SELECT * from recipe
    WHERE recipe.recipe_id in (SELECT creates.recipe_id FROM creates WHERE creates.user_id = {});   
    """.format(user_id)

    cursor.execute(command)
    response = cursor.fetchall()

    recipes = []

    if len(response) > 0 :     
        for data in response:
            recipes.append(Recipe(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4]
            ))

    return recipes

def getUserIngredient(user_id):
    cursor = db.cursor()

    command = """
    SELECT ingredients.ingredient_id, ingredients.name, ingr_unit.unit, ingr_quan.quantity
    FROM (SELECT stores.ingredient_id, stores.quantity
            FROM stores
            WHERE stores.user_id = {}) ingr_quan

    LEFT JOIN ingredients
    ON ingr_quan.ingredient_id = ingredients.ingredient_id

    LEFT JOIN (SELECT measured_in.ingredient_id , measurement.unit
                FROM measured_in
                LEFT JOIN measurement
                on measured_in.measurement_id = measurement.measurement_id)as ingr_unit
    on ingr_quan.ingredient_id = ingr_unit.ingredient_id
    """.format(user_id)

    cursor.execute(command)
    response = cursor.fetchall()

    ingredients = []

    if len(response) > 0 :     
        for data in response:
            ingredients.append(Ingredient(
                data[0],
                data[1],
                data[2],
                data[3]
            ))

    return ingredients

def getUserMealPlans(user_id):
    cursor = db.cursor()

    command = """
    SELECT * from meal_plan WHERE meal_plan.mealplan_id in (SELECT schedule.mealplan_id from schedule WHERE schedule.user_id = %s);   
    """

    cursor.execute(command, (user_id,))
    response = cursor.fetchall()

    mealplans = []

    if len(response) > 0 :     
        for data in response:
            mp = MealPlan(
                data[0],
                data[1],
                data[2],
            )
            mealplans.append(mp)
    return mealplans

def getMealPlanMeals(mealplan_id):
    cursor = db.cursor()

    command_lunch = """
    SELECT lunch.meal_id from lunch WHERE lunch.mealplan_id = {};
    """.format(mealplan_id)
    command_dinner = """
    SELECT dinner.meal_id from dinner WHERE dinner.mealplan_id = {};
    """.format(mealplan_id)
    command_breakfast = """
    SELECT breakfast.meal_id from breakfast WHERE breakfast.mealplan_id = {};
    """.format(mealplan_id)

    meals = []
    lunch_id = None
    breakfast_id = None
    dinner_id = None

    # Get Lunch
    cursor.execute(command_lunch)
    response = cursor.fetchall()

    if len(response) > 0 :  
        lunch_id = response[0][0]
        meal = getMeal(lunch_id)
        meals.append(meal)
    
    # Get dinner
    cursor.execute(command_dinner)
    response = cursor.fetchall()

    if len(response) > 0 :  
        dinner_id = response[0][0]
        meal = getMeal(dinner_id)
        meals.append(meal)
    
    # Get breakfast
    cursor.execute(command_breakfast)
    response = cursor.fetchall()

    if len(response) > 0 :  
        breakfast_id = response[0][0]
        meal = getMeal(breakfast_id)
        meals.append(meal)

    return meals, (lunch_id, dinner_id, breakfast_id)

"""
import files for testing
from databasemanager import *
from models import *
"""