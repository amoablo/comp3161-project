-- Meal Planner Fake Data and tables

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


-- Insert Users data

insert into users (first_name, last_name, email, gender, password) values ( 'Brenda', 'Casey', 'wilkersonpamela@yahoo.com', 'M', '_3_kKjhgk)');
insert into users (first_name, last_name, email, gender, password) values ( 'John', 'Thompson', 'toddbrown@phillips.net', 'M', 'e21P1XWq)W');

-- Insert recipe data

insert into recipe (name, created_date) values ( 'Himself push sell account.', '2019-10-18');
insert into recipe (name, created_date) values ( 'Professor ability analysis hotel.', '2019-06-09');

-- Insert ingredients data

insert into ingredients (name) values ( 'Resource.');
insert into ingredients (name) values ( 'If suffer.');
insert into ingredients (name) values ( 'Imagine.');
insert into ingredients (name) values ( 'Other.');
insert into ingredients (name) values ( 'Morning.');

-- Insert measurement data

insert into measurement (unit) values ( 'count');
insert into measurement (unit) values ( 'lb');

-- Insert measured in data

insert into measured_in (ingredient_id, measurement_id) values ( '0', '0');
insert into measured_in (ingredient_id, measurement_id) values ( '1', '1');
insert into measured_in (ingredient_id, measurement_id) values ( '2', '1');
insert into measured_in (ingredient_id, measurement_id) values ( '3', '0');
insert into measured_in (ingredient_id, measurement_id) values ( '4', '0');

-- Insert made of data

insert into made_of (recipe_id, ingredient_id, amount) values ( '0', '3', '4');
insert into made_of (recipe_id, ingredient_id, amount) values ( '0', '4', '2');
insert into made_of (recipe_id, ingredient_id, amount) values ( '1', '4', '7');
insert into made_of (recipe_id, ingredient_id, amount) values ( '1', '3', '4');

-- Insert instruction data

insert into instrctions (step_no, step_description) values ( '1', 'Again health on read court land two.');
insert into instrctions (step_no, step_description) values ( '1', 'Information system free street person good.');

-- Insert prepare data

insert into prepare (recipe_id, instruction_id, step_no) values ( '0', '0', '1');
insert into prepare (recipe_id, instruction_id, step_no) values ( '1', '1', '1');
