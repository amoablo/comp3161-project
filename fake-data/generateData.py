from faker import Faker
from faker.providers import BaseProvider
import random



# Create the tables in the sql file

meal_planner_fake_sql = """-- Meal Planner Fake Data and tables

/* clean up old tables;
   must drop tables with foreign keys first
   due to referential integrity constraints
 */
drop table IF EXISTS users cascade;
drop table IF EXISTS meal_plan cascade;
drop table IF EXISTS meal cascade;
drop table IF EXISTS recipe cascade;
drop table IF EXISTS instructions cascade;
drop table IF EXISTS ingredients cascade;
drop table IF EXISTS measurement cascade;
drop table IF EXISTS made_of;
drop table IF EXISTS stores;
drop table IF EXISTS schedule;
drop table IF EXISTS breakfast;
drop table IF EXISTS lunch;
drop table IF EXISTS dinner;
drop table IF EXISTS made_from;
drop table IF EXISTS prepare;
drop table IF EXISTS measured_in;

-- Table creations 

create table users(
	user_id int not null unique auto_increment,
	first_name varchar(50),
    last_name varchar(50), 
    email varchar(100) unique,
    gender char(1),
    password text,
	primary key(user_id)
);

create table meal_plan(
    mealplan_id int not null unique auto_increment,
    meal_date date,
    week_num int,
    primary key(mealplan_id)
);

create table meal(
    meal_id int not null unique auto_increment,
    calorie int,
    num_servings int(6),
    image_url text,
    primary key(meal_id)
);

create table recipe(
    recipe_id int not null unique auto_increment,
    name varchar(255),
    created_date date,
    primary key(recipe_id)
);

create table instructions(
    instruction_id int not null unique auto_increment,
    step_no int,
    step_description text,
    primary key(instruction_id, step_no)
);

create table ingredients(
    ingredient_id int not null unique auto_increment,
    name varchar(200),
    primary key(ingredient_id)
);

create table measurement(
    measurement_id int not null unique auto_increment,
    unit varchar(30),
    primary key(measurement_id)
);

create table made_of(
    recipe_id int not null,
    ingredient_id int not null,
    amount int,
    foreign key(recipe_id) references recipe(recipe_id) on delete cascade,
    foreign key(ingredient_id) references ingredients(ingredient_id) on delete cascade
);

create table stores(
    user_id int not null,
    ingredient_id int not null,
    quantity int, 
    foreign key(user_id) references users(user_id) on delete cascade,
    foreign key(ingredient_id) references ingredients(ingredient_id) on delete cascade
);

create table schedule(
    user_id int not null,
    mealplan_id int not null,
    schedule_date date,
    foreign key(user_id) references users(user_id) on delete cascade,
    foreign key(mealplan_id) references meal_plan(mealplan_id) on delete cascade
);

create table breakfast(
    meal_id int not null,
    breakfast_date date,
    foreign key(meal_id) references meal(meal_id) on delete cascade
);

create table lunch(
    meal_id int not null,
    lunch_date date,
    foreign key(meal_id) references meal(meal_id) on delete cascade
);

create table dinner(
    meal_id int not null,
    dinner_date date,
    foreign key(meal_id) references meal(meal_id) on delete cascade
);

create table made_from(
    meal_id int not null,
    recipe_id int not null,
    foreign key(meal_id) references meal(meal_id) on delete cascade,
    foreign key(recipe_id) references recipe(recipe_id) on delete cascade
);

create table prepare(
    recipe_id int not null,
    instruction_id int not null,
    step_no int not null,
    foreign key(recipe_id) references recipe(recipe_id) on delete cascade,
    foreign key(instruction_id, step_no) references instructions(instruction_id, step_no) on delete cascade
);

create table measured_in(
    ingredient_id int not null,
    measurement_id int not null, 
    foreign key(ingredient_id) references ingredients(ingredient_id) on delete cascade,
    foreign key(measurement_id) references measurement(measurement_id) on delete cascade
);

-- Stored Procedures
DELIMITER //

-- Procedures go here 

-- CREATE PROCEDURE Testi()
-- BEGIN
-- 	SELECT *  FROM products;
-- END //

DELIMITER ;

-- Insertions

"""

# Generate the fake data 


# data dictionary
fake_data = {
    "user":{
        "fname":[],
        "lname":[],
        "email":[],
        "gender":[],
        "password":[]
    },
    "meal_plan":{
        "date":[],
        "week_num":[]
    },
    "meal":{
        "calorie":[],
        "num_servings":[],
        "image_url":[]
    },
    "recipe":{
        "name":[],
        "date":[],
    },
    "instruction":{
        "step_no":[],
        "description":[]
    },
    "ingredient":{
        "name":[]
    },
    "measurement":{
        "unit":[]
    },
    "made_of":{
        "recipe_id":[],
        "ingredient_id":[],
        "amount":[]
    },
    "stores":{
        "user_id":[],
        "ingredient_id":[],
        "quantity":[]
    },
    "schedule":{
        "user_id":[],
        "mealplan_id":[],
        "date":[]
    },
    "breakfast":{
        "date":[],
        "meal_id":[]
    },
    "lunch":{
        "date":[],
        "meal_id":[]
    },
    "dinner":{
        "date":[],
        "meal_id":[]
    },
    "made_from":{
        "meal_id":[],
        "recipe_id":[]
    },
    "prepare":{
        "recipe_id":[],
        "instruction_id":[],
        "step_no":[]
    },
    "measured_in":{
        "ingredient_id":[],
        "measurement_id":[]
    }

}

# Fake data Configuration Variables

# num_fake_users = 200000
# num_fake_recipes = 600000
num_fake_users = 2
num_fake_recipes = 6
num_ingredients = 20
max_num_recipe_ingredient = 8 #this needs to be less than or equal to the num_ingredients
max_ingredient_amount = 10
max_instructions_steps = 7




fake = Faker(['en-US', 'en_US', 'en_US', 'en-US'])
Faker.seed(129)

# ===========================
#   populate user table 
#============================


# create new provider class
class userProvider(BaseProvider):
    def gender(self):
        return random.choice(["M","F","O"])
    
fake.add_provider(userProvider)

for _ in range(num_fake_users):
    fake_data["user"]["fname"].append( fake.first_name() )
    fake_data["user"]["lname"].append( fake.last_name() )
    fake_data["user"]["email"].append( fake.unique.email() )
    fake_data["user"]["gender"].append( fake.gender() )
    fake_data["user"]["password"].append( fake.password() )

# print(fake_data["user"])

# ===========================
#   populate recipe table 
#============================


for _ in range(num_fake_recipes):
    fake_data["recipe"]["name"].append( fake.text(max_nb_chars=50 ))
    fake_data["recipe"]["date"].append( fake.date_between(start_date='-5y') )



# ===========================
#   populate ingredient table 
#============================

for _ in range(num_ingredients):
    fake_data["ingredient"]["name"].append( fake.text(max_nb_chars=10 ))


# ===========================
#   populate measurement table 
#============================

fake_data["measurement"]["unit"] = ["count","lb"]



# ===========================
#   populate measureed in table 
#============================

for i_id in range(len(fake_data["ingredient"]["name"])):
    fake_data["measured_in"]["ingredient_id"].append(i_id+1)
    fake_data["measured_in"]["measurement_id"].append(random.randint(1,len(fake_data["measurement"]["unit"])))



# ===========================
#   populate made_of table 
#============================

for r_id in range(len(fake_data["recipe"]["name"])):
    ingredients_id = random.sample(range(num_ingredients), max_num_recipe_ingredient)
    for i_id in ingredients_id:
        fake_data["made_of"]["recipe_id"].append(r_id+1)
        fake_data["made_of"]["ingredient_id"].append(i_id+1)
        fake_data["made_of"]["amount"].append(random.randint(1, max_ingredient_amount-1))
    



# ===========================
#   populate prepare and instruction id table 
#============================



inst_id = 0
for r_id in range(len(fake_data["recipe"]["name"])):
    for steps in range(random.randint(1,max_instructions_steps)):
        fake_data["prepare"]["recipe_id"].append(r_id+1)
        fake_data["prepare"]["instruction_id"].append(inst_id+1)
        fake_data["prepare"]["step_no"].append(steps+1)
        fake_data["instruction"]["step_no"].append(steps+1)
        fake_data["instruction"]["description"].append(fake.text(max_nb_chars=50 ))
        inst_id+=1

# insert the data into the sql

# insert users

meal_planner_fake_sql += """
-- Insert Users data

"""

for indx in range(len(fake_data["user"]["fname"])):
    insert_command = """insert into users (first_name, last_name, email, gender, password) values ( '{}', '{}', '{}', '{}', '{}');
""".format(
        fake_data["user"]["fname"][indx],
        fake_data["user"]["lname"][indx],
        fake_data["user"]["email"][indx],
        fake_data["user"]["gender"][indx],
        fake_data["user"]["password"][indx]
    )
    meal_planner_fake_sql+= insert_command


# insert recipes

meal_planner_fake_sql += """
-- Insert recipe data

"""

for indx in range(len(fake_data["recipe"]["name"])):
    insert_command = """insert into recipe (name, created_date) values ( '{}', '{}');
""".format(
        fake_data["recipe"]["name"][indx],
        fake_data["recipe"]["date"][indx]
    )
    meal_planner_fake_sql+= insert_command



# insert ingredients

meal_planner_fake_sql += """
-- Insert ingredients data

"""

for indx in range(len(fake_data["ingredient"]["name"])):
    insert_command = """insert into ingredients (name) values ( '{}');
""".format(
        fake_data["ingredient"]["name"][indx]
    )
    meal_planner_fake_sql+= insert_command


# insert measurement

meal_planner_fake_sql += """
-- Insert measurement data

"""

for indx in range(len(fake_data["measurement"]["unit"])):
    insert_command = """insert into measurement (unit) values ( '{}');
""".format(
        fake_data["measurement"]["unit"][indx]
    )
    meal_planner_fake_sql+= insert_command



# insert instruction

meal_planner_fake_sql += """
-- Insert instruction data

"""

for indx in range(len(fake_data["instruction"]["step_no"])):
    insert_command = """insert into instructions (step_no, step_description) values ( '{}', '{}');
""".format(
        fake_data["instruction"]["step_no"][indx],
        fake_data["instruction"]["description"][indx],
    )
    meal_planner_fake_sql+= insert_command





# insert measured in

meal_planner_fake_sql += """
-- Insert measured in data

"""

for indx in range(len(fake_data["measured_in"]["ingredient_id"])):
    insert_command = """insert into measured_in (ingredient_id, measurement_id) values ( '{}', '{}');
""".format(
        fake_data["measured_in"]["ingredient_id"][indx],
        fake_data["measured_in"]["measurement_id"][indx]
    )
    meal_planner_fake_sql+= insert_command

# insert measured in

# meal_planner_fake_sql += """
# -- Insert measured in data

# """

# for indx in range(len(fake_data["measured_in"]["ingredient_id"])):
#     insert_command = """insert into measured_in (ingredient_id, measurement_id)values ( (select ingredient_id from ingredients where ingredient_id = {}), (select measurement_id from measurement where measurement_id = {}));
# """.format(
#         fake_data["measured_in"]["ingredient_id"][indx],
#         fake_data["measured_in"]["measurement_id"][indx]
#     )
#     meal_planner_fake_sql+= insert_command



# insert made of

meal_planner_fake_sql += """
-- Insert made of data

"""

for indx in range(len(fake_data["made_of"]["recipe_id"])):
    insert_command = """insert into made_of (recipe_id, ingredient_id, amount) values ( '{}', '{}', '{}');
""".format(
        fake_data["made_of"]["recipe_id"][indx],
        fake_data["made_of"]["ingredient_id"][indx],
        fake_data["made_of"]["amount"][indx]
    )
    meal_planner_fake_sql+= insert_command



# insert prepare

meal_planner_fake_sql += """
-- Insert prepare data

"""

for indx in range(len(fake_data["prepare"]["recipe_id"])):
    insert_command = """insert into prepare (recipe_id, instruction_id, step_no) values ( '{}', '{}', '{}');
""".format(
        fake_data["prepare"]["recipe_id"][indx],
        fake_data["prepare"]["instruction_id"][indx],
        fake_data["prepare"]["step_no"][indx]
    )
    meal_planner_fake_sql+= insert_command



# Write the string to the sql file 
text_file = open("meal_planer_fake_data.sql", "w")
text_file.write(meal_planner_fake_sql)
text_file.close()
