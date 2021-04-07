import os, random
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, Markup
from flask_login import login_user, logout_user, current_user, login_required
from flask.helpers import send_from_directory
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from .forms import *
import os, random
from flask.helpers import send_from_directory
from app.models import *
from .models import *
import pymysql
from datetime import datetime



@app.route('/')
def home():
    """Render website's home page."""
    return render_template('index.html')

@app.route('/recipes')
def recipes():
    """Render website's recipes page."""
    con = db_connect()
    cur=con.cursor()
    cur.execute("select * from recipe")
    recipieList = list(cur.fetchall())
    cur.close()
    con.close()
    return render_template('recipes.html',recipes=recipieList)

@app.route('/myRecipes/<recipieid>')
def getIndividualRecipe(recipieid):
    recipe = getRecipe(recipieid)
    recipe.setInstructions()
    recipe.setIngredients()
    instructions = recipe.instructions
    print(instructions)
    ingredients = recipe.ingredients
    print(ingredients)
    
     if recipe  is None:
         return redirect(url_for('home'))
    return render_template("recipie_view.html", recipe=recipe, instructions =instructions, ingredients=ingredients)


@app.route('/myRecipes')
#@login_required
def myRecipes():
    """Render website's Personal Recipes Uploaded, My Recipes page."""
    current_user.setRecipes()
    recipieList =  current_user.recipes
    for i in recipieList:
        if 'http' not in i.image_url:
            i.image_url= url_for('getImage', filename=i.image_url)
    return render_template('myRecipes.html',lst = recipieList)

@app.route("/addRecipe", methods=["GET", "POST"])
def addRecipe():
    form = RecipeForm()
    if request.method == "POST" and form.validate_on_submit():

        name = form.name.data 
        calories = form.calories.data
        number_of_steps = form.number_of_steps.data
        step_description = form.step_description.data
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        date = datetime.today().strftime('%Y-%m-%d')

        con = db_connect()
        cur=con.cursor()
        recipe = 'insert into recipe values(%s %s %s);'
        cur.execute(recipe,name,date,filename)
        for i in number_of_steps:
            instruction = 'insert into instructions values(%s %s);'
            cur.execute(instruction,i,instruction)

        cur.close()
        con.close()

        flash('Recipie Saved', 'success')
        return redirect('/myRecipes')
    else:
        flash_errors(form)
    return render_template('addRecipe.html',form=form)


@app.route('/mealPlan', methods=['GET','POST'])
@login_required
def mealPlan():
    """Render website's meal plan page."""
    form = MealPlanForm()
    connection = db_connect()
    if connection is not None:
        cursor = connection.cursor()
        if request.method == "POST" and form.validate_on_submit():
            user_id = current_user.get_id()
            sql = "SELECT * FROM recipe WHERE recipe_id in (SELECT recipe_id FROM creates WHERE user_id = %s);"
            cursor.execute(sql, (user_id,))
            recipes = cursor.fetchall()
            calories = form.calories.data
            not_found = True
            total_calories = 0
            days = {}
            day = 1
            threshold = calories // 7 # because there are 3 meals in a day
            """
                For each day, find meals that meet the weekly 
                calories divided by 7.
            """
            while day <= 7:
                days[day] = find_days(recipes, threshold)
                day += 1
            print(days)
            sql = "SELECT mealplan_id FROM schedule WHERE user_id = %s;"
            cursor.execute(sql, (current_user.get_id()))
            plan_id = cursor.fetchone()
            plan_id = plan_id["mealplan_id"]
            for d in days:
                i = 0
                for meal in days[d]:
                    if meal != []:
                        sql = "INSERT INTO meal(calorie, num_servings) VALUES (%s, %s);"
                        cursor.execute(sql, (meal[0]["calorie"], meal[1]))
                        sql = "SELECT meal_id FROM meal WHERE calorie = %s and num_servings = %s;"
                        cursor.execute(sql, (meal[0]["calorie"], meal[1]))
                        meal_id = cursor.fetchone()
                        meal_id = meal_id["meal_id"]
                        sql = "INSERT INTO made_from(meal_id, recipe_id) VALUES (%s, %s);"
                        cursor.execute(sql, (meal_id, meal[0]["recipe_id"]))
                        connection.commit()
                        if i == 0:
                            sql = "INSERT INTO breakfast VALUES (%s, %s);"
                            cursor.execute(sql, (meal_id, plan_id))
                        elif i == 1:
                            sql = "INSERT INTO lunch VALUES (%s, %s);"
                            cursor.execute(sql, (meal_id, plan_id))
                        elif i == 2:
                            sql = "INSERT INTO dinner VALUES (%s, %s);"
                            cursor.execute(sql, (meal_id, plan_id))
                    connection.commit()
                    i += 1
            # close connection
            cursor.close()
            connection.close()
            flash("Your meal plan has been generated", "success")
            return redirect('/mealPlan')
        # else
        sql = "SELECT recipe.*, meal.num_servings FROM recipe, meal WHERE (recipe_id, meal_id) IN (SELECT DISTINCT recipe_id, meal_id FROM made_from WHERE meal_id IN(SELECT meal_id FROM breakfast WHERE mealplan_id IN (SELECT mealplan_id FROM meal_plan WHERE mealplan_id in (SELECT mealplan_id FROM schedule WHERE user_id = %s))));"
        cursor.execute(sql, (current_user.get_id()))
        breakfast = cursor.fetchall()
        sql = "SELECT recipe.*, meal.num_servings FROM recipe, meal WHERE (recipe_id, meal_id) IN (SELECT DISTINCT recipe_id, meal_id FROM made_from WHERE meal_id IN(SELECT meal_id FROM lunch WHERE mealplan_id IN (SELECT mealplan_id FROM meal_plan WHERE mealplan_id in (SELECT mealplan_id FROM schedule WHERE user_id = %s))));"
        cursor.execute(sql, (current_user.get_id()))
        lunch = cursor.fetchall()
        sql = "SELECT recipe.*, meal.num_servings FROM recipe, meal WHERE (recipe_id, meal_id) IN (SELECT DISTINCT recipe_id, meal_id FROM made_from WHERE meal_id IN(SELECT meal_id FROM dinner WHERE mealplan_id IN (SELECT mealplan_id FROM meal_plan WHERE mealplan_id in (SELECT mealplan_id FROM schedule WHERE user_id = %s))));"
        cursor.execute(sql, (current_user.get_id()))
        dinner = cursor.fetchall() 
        cursor.close()
        connection.close()
        # collapse into one dictionary
        length = len(breakfast) + len(lunch) +len(dinner)
        plan = {"breakfast":breakfast, "lunch":lunch, "dinner":dinner}
        calories = 0
        for subplan in plan.values():
            for meal in subplan:
                calories += meal['calorie'] * meal['num_servings']
        
        return render_template('mealplan.html',total_calories=calories, length=length, plan=plan, form=form)
    flash("Can't connect to database","danger")
    return redirect(url_for('login'))

@app.route('/pantry')
# @login_required
def pantry():
    """Render website's pantry page."""
    conn = db_connect()
    with conn:
        with conn.cursor() as cursor:
            sql_query = "select quantity, name, unit from users as u \
                join stores as s on u.user_id=s.user_id \
                    join ingredients as i on s.ingredient_id=i.ingredient_id \
                        join measured_in as mi on i.ingredient_id=mi.ingredient_id \
                            join measurement as m on mi.measurement_id=m.measurement_id"
            cursor.execute(sql_query)
            result = (cursor.fetchall())
            if result is None:
                return redirect(url_for('home'))
    return render_template('pantry.html', ingredients=result)


@app.route('/shoppingList')
#@login_required
def shoppingList():
    ingredients = []
    if current_user.is_authenticated:
        current_user.setShoppingList()
        ingredients = current_user.shoppingList
    else:
        flash('You need to login first.', 'danger')   
    """Render website's shopping list page."""
    return render_template('shoppinglist.html', Shopping_ingredients=ingredients)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('recipes'))
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Get the username and password values from the form.
            email = form.email.data
            password = form.password.data

            # query database for a user based on the username
            connection = db_connect()
            if connection is not None:
                cursor = connection.cursor()
                sql = "SELECT * FROM users WHERE email = %s and password = %s"
                cursor.execute(sql, (email, password))
                user = cursor.fetchone()
                # validate the password and ensure that a user was found
                if user is not None and user["password"] == password:
                    user = User(user["user_id"], user["first_name"], user["last_name"], user["email"], user["gender"], user["password"])
                    login_user(user)    # load into session
                    flash('Logged in successfully.', 'success') # flash a message to the user
                    return redirect(request.url)  # redirect to a secure-page route
                else:
                    flash('Username or Password is incorrect.', 'danger')
                cursor.close()
            else:
                flash("Can't connect to database.","danger")
            connection.close()
    flash_errors(form)
    return render_template("login.html", form=form)


@app.route("/join", methods=["GET", "POST"])
def join():
    if current_user.is_authenticated:
        return redirect(url_for('recipe'))
    form = SignUpForm()

    if request.method == "POST":
        if form.validate_on_submit():
            # Get the username and password values from the form.
            firstname=form.firstname.data
            lastname=form.lastname.data
            gender = request.form['genderOptions']
            email = form.email.data
            password = form.password.data
            
            con = db_connect()
            cur=con.cursor()
            sql="INSERT INTO users(first_name,last_name,email,gender,password) VALUES(%s,%s,%s,%s,%s)"
            cur.execute(sql,(firstname,lastname,email,gender,password))
            con.commit()
            cur.close()
            con.close()
            flash('Joined successfully.', 'success')
            return redirect(url_for("login"))
        else:
            flash('Information invalid.', 'danger')
            # query database for a user based on the username

            # user = ''

            # # validate the password and ensure that a user was found
            # if user is not None and check_password_hash(user.password, password):
            #     login_user(user)    # load into session
            #     flash('Joined successfully.', 'success') # flash a message to the user
            #     return redirect(url_for("recipes"))  # redirect to a secure-page route
            # else:
            #     flash('Username or Password is incorrect.', 'danger')
    flash_errors(form)
    return render_template("join.html", form=form)


@app.route("/logout")
@login_required
def logout():
    # Logs out the user and ends the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    connection = db_connect()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE user_id = %s;"
            cursor.execute(sql, (id))
            user = cursor.fetchone()
            if user is not None:
                return User(user["user_id"], user["first_name"], user["last_name"], user["email"], user["gender"], user["password"])
    return None

def db_connect():
    '''Connects to mysql database using environment variables'''
    return pymysql.connect(host=app.config['DATABASE_HOST'],
                             user=app.config['DATABASE_USER'],
                             password=app.config['DATABASE_PASSWORD'],
                             database=app.config['DATABASE_NAME'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def find_days(recipes, calories):
    seed = random.randrange(0, len(recipes))
    total_calories = 0
    i = 0
    result = [[],[],[]]
    while total_calories < calories and i < 10:
        # print(result)
        seed = random.randrange(0, len(recipes))
        if result[i%3] == []:
            if total_calories + recipes[seed]["calorie"] <= calories:
                total_calories += recipes[seed]["calorie"]
                result[i%3].append(recipes[seed])
                result[i%3].append(1)
        elif total_calories + result[i%3][0]["calorie"] <= calories:
            total_calories += result[i%3][0]["calorie"]
            result[i%3][1] += 1 
        else:
            break
        i += 1
    return result

@app.route('/recipes/<filename>')
def getImage(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER_RECIPE']),filename)

def get_uploaded_images():
    uploaded_images = []
    rootdir = os.getcwd()
    for subdir, dirs, files in os.walk(rootdir + app.config['UPLOAD_FOLDER_RECIPE']):
        for filename in files:
            uploaded_images.append(filename)
    return uploaded_images





# Flash errors from the form if validation fails with Flask-WTF
# http://flask.pocoo.org/snippets/12/
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error), 'danger')

###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")