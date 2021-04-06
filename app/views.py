from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, Markup
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from .forms import LoginForm,SignUpForm,MealPlanForm
import os
from flask.helpers import send_from_directory
from app.models import User
import pymysql


def db_connect():
    '''Connects to mysql database using environment variables'''
    return pymysql.connect(host=app.config['DATABASE_HOST'],
                             user=app.config['DATABASE_USER'],
                             password=app.config['DATABASE_PASSWORD'],
                             database=app.config['DATABASE_NAME'],
                             cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('index.html')

@app.route('/recipes')
def recipes():
    """Render website's recipes page."""
    #images = get_uploaded_images()
    #connect to the db
    con = db_connect()
    #cursor (two cursor server side and client side)
    cur=con.cursor()
    #execute
    cur.execute("select * from recipe")
    # returns array of tuples
    #rows=cur.fetchall()
    recipieList = list(cur.fetchall())
    print(recipieList)
    #for r in rows:
     #   print(f"Name:{r[1]}  Date: {r[2]}")
    cur.close()
    #close the connection
    con.close()
    return render_template('recipes.html',recipes=recipieList)

@app.route('/myRecipes/<recipieid>')
def getRecipe(recipieid):
    con = db_connect()
    cur=con.cursor()
    stat = "select recipe.name,recipe.created_date,instructions.step_no,instructions.step_description from recipe join prepare on recipe.recipe_id=prepare.recipe_id join instructions on instructions.instruction_id=prepare.instruction_id and recipe.recipe_id= %s"
    ing = "select ingredients.name,made_of.amount from ingredients join made_of on ingredients.ingredient_id=made_of.ingredient_id join recipe on recipe.recipe_id=made_of.recipe_id and recipe.recipe_id= %s"
    cur.execute(stat,recipieid)
    query = list(cur.fetchall())
    cur.execute(ing,recipieid)
    query2 = list(cur.fetchall())
    name = query[0][0]
    date = query[0][1]
    lst = [name,date]
    lst2 = []
    for i in query:
        lst2.append([i[2],i[3]])
    print(query2)
    cur.close()
    con.close()
    if query  is None:
        return redirect(url_for('home'))
    return render_template("recipie_view.html", query=lst, lst2 =lst2, query2=query2)


@app.route('/myRecipes')
#@login_required
def myRecipes():
    """Render website's Personal Recipes Uploaded, My Recipes page."""
    #connect to the db
    con = db_connect()
    #cursor (two cursor server side and client side)
    cur=con.cursor()
    #execute
    cur.execute("select * from recipe")
    # returns array of tuples
    #rows=cur.fetchall()
    recipieList = list(cur.fetchall())
    print(recipieList)
    #for r in rows:
     #   print(f"Name:{r[1]}  Date: {r[2]}")
    cur.close()
    #close the connnection
    con.close()
    return render_template('myRecipes.html',lst = recipieList)

@login_required
@app.route('/mealPlan', methods=['GET','POST'])
# @login_required
def mealPlan():
    """Render website's meal plan page."""
    form = MealPlanForm()
    connection = db_connect()
    if connection is not None:
        cursor = connection.cursor()
        if request.method == "GET":
            user_id = current_user.get_id()
            sql = "SELECT * FROM recipe WHERE recipe_id in (SELECT recipe_id FROM creates WHERE user_id = %s);"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchall()
            calories = form.calories.data
            not_found = True
            print(result)
            # while not_found:
            #     random.randrange(1, length(result))
            return render_template('mealplan.html', plan=result)
        sql = "SELECT * FROM recipes;"
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
        result = cursor.fetchone()
        cursor.close()
    connection.close()
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
    
    """Render website's shopping list page."""
    return render_template('shoppinglist.html')

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
            gender=form.gender.data
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
def load_user(user_id):
    connection = db_connect()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(sql, (user_id))
            user = cursor.fetchone()
            if user is not None:
                return User(user["user_id"], user["first_name"], user["last_name"], user["email"], user["gender"], user["password"])
    return None

# Connect to the database
def db_connect():
    return pymysql.connect(host=app.config['DATABASE_HOST'],
                             user=app.config['DATABASE_USER'],
                             password=app.config['DATABASE_PASSWORD'],
                             database=app.config['DATABASE_NAME'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


@app.route('/recipes/<filename>')
def getImage(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, './uploads'),filename)

def get_uploaded_images():
    uploaded_images = []
    rootdir = os.getcwd()
    for subdir, dirs, files in os.walk(rootdir + '/uploads'):
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