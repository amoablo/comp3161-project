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

insert into users (first_name, last_name, email, gender, password) values ('fname', 'lname',	'fname@ds.com','M', 'asdfsdasd');

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


# num_fake_users = 200000
# num_fake_recipes = 600000
num_fake_users = 2
num_fake_recipes = 6

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


print(fake_data["ingredient"])

for _ in range(num_fake_recipes):
    fake_data["ingredient"]["name"].append( fake.text(max_nb_chars=50 ))
    fake_data["recipe"]["date"].append( fake.date_between(start_date='-5y') )

# Write the string to the sql file 
text_file = open("meal_planer_fake_data.sql", "w")
text_file.write(meal_planner_fake_sql)
text_file.close()