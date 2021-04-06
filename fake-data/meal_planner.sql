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
    calorie int,
    image_url text,
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

create table creates(
    user_id int not null,
    recipe_id int not null, 
    foreign key(user_id) references users(user_id) on delete cascade,
    foreign key(recipe_id) references recipe(recipe_id) on delete cascade
);

-- Stored Procedures
DELIMITER //

-- Procedures go here 

-- CREATE PROCEDURE Testi()
-- BEGIN
-- 	SELECT *  FROM products;
-- END //

DELIMITER ;

-- =========================
--       Insertions
-- =========================


-- Insert Users data

insert into users (first_name, last_name, email, gender, password) values ( 'Brenda', 'Casey', 'wilkersonpamela@yahoo.com', 'F', '_3_kKjhgk)');
insert into users (first_name, last_name, email, gender, password) values ( 'John', 'Thompson', 'toddbrown@phillips.net', 'O', 'e21P1XWq)W');
insert into users (first_name, last_name, email, gender, password) values ( 'Gregory', 'Johns', 'perezjason@weaver.org', 'M', '!$H2V1gcH&');
insert into users (first_name, last_name, email, gender, password) values ( 'Wayne', 'Mendoza', 'saguilar@hotmail.com', 'M', '37mP(azK$K');
insert into users (first_name, last_name, email, gender, password) values ( 'Robert', 'Phelps', 'michael43@hotmail.com', 'O', '*bxLziTB2I');

-- Insert recipe data

insert into recipe (name, created_date, calorie, image_url) values ( 'Hold man likely since.', '2016-05-06', '310', 'https://placekitten.com/98/673');
insert into recipe (name, created_date, calorie, image_url) values ( 'Necessary family behind trial.', '2018-12-29', '271', 'https://placekitten.com/724/857');
insert into recipe (name, created_date, calorie, image_url) values ( 'Identify as seat garden few.', '2017-03-13', '267', 'https://dummyimage.com/37x45');
insert into recipe (name, created_date, calorie, image_url) values ( 'Moment animal human form together.', '2018-09-10', '356', 'https://www.lorempixel.com/184/532');
insert into recipe (name, created_date, calorie, image_url) values ( 'Series catch win month.', '2018-03-19', '357', 'https://placekitten.com/72/977');
insert into recipe (name, created_date, calorie, image_url) values ( 'Unit mention all health become.', '2018-03-17', '1297', 'https://dummyimage.com/761x1004');
insert into recipe (name, created_date, calorie, image_url) values ( 'Into agent morning both.', '2019-04-27', '1644', 'https://placeimg.com/27/842/any');
insert into recipe (name, created_date, calorie, image_url) values ( 'Our scene firm floor.', '2019-06-02', '889', 'https://dummyimage.com/314x68');
insert into recipe (name, created_date, calorie, image_url) values ( 'Phone particular policy happy national culture.', '2020-04-28', '296', 'https://placekitten.com/1012/582');
insert into recipe (name, created_date, calorie, image_url) values ( 'Doctor around site shoulder we.', '2019-09-12', '1017', 'https://placekitten.com/558/831');

-- Insert ingredients data

insert into ingredients (name) values ( 'Home wall.');
insert into ingredients (name) values ( 'Likely.');
insert into ingredients (name) values ( 'Security.');
insert into ingredients (name) values ( 'Order cut.');
insert into ingredients (name) values ( 'Hotel.');
insert into ingredients (name) values ( 'Difficult.');
insert into ingredients (name) values ( 'Paper.');
insert into ingredients (name) values ( 'Business.');
insert into ingredients (name) values ( 'Stop.');
insert into ingredients (name) values ( 'Many.');
insert into ingredients (name) values ( 'Above.');
insert into ingredients (name) values ( 'Next.');
insert into ingredients (name) values ( 'Must.');
insert into ingredients (name) values ( 'Person.');
insert into ingredients (name) values ( 'Training.');
insert into ingredients (name) values ( 'Rule.');
insert into ingredients (name) values ( 'Goal.');
insert into ingredients (name) values ( 'Meeting.');
insert into ingredients (name) values ( 'Short.');
insert into ingredients (name) values ( 'Actually.');

-- Insert measurement data

insert into measurement (unit) values ( 'count');
insert into measurement (unit) values ( 'gallon');
insert into measurement (unit) values ( 'lb');
insert into measurement (unit) values ( 'litre');
insert into measurement (unit) values ( 'kg');
insert into measurement (unit) values ( 'teaspoon');
insert into measurement (unit) values ( 'tablespoon');
insert into measurement (unit) values ( 'cup');
insert into measurement (unit) values ( 'quart');
insert into measurement (unit) values ( 'pound');

-- Insert instruction data

insert into instructions (step_no, step_description) values ( '1', 'Culture sure assume close analysis law truth.');
insert into instructions (step_no, step_description) values ( '2', 'Yet note fund account however.');
insert into instructions (step_no, step_description) values ( '3', 'Old right wife make strong condition.');
insert into instructions (step_no, step_description) values ( '4', 'Heavy understand author public loss.');
insert into instructions (step_no, step_description) values ( '1', 'Care response skill source per discover.');
insert into instructions (step_no, step_description) values ( '2', 'Standard level experience later five from.');
insert into instructions (step_no, step_description) values ( '3', 'Kind many test thing too site sport laugh.');
insert into instructions (step_no, step_description) values ( '4', 'Now television data. Majority learn human huge.');
insert into instructions (step_no, step_description) values ( '5', 'Deal see should camera bring consider ground.');
insert into instructions (step_no, step_description) values ( '1', 'Skill across even actually.');
insert into instructions (step_no, step_description) values ( '2', 'Into city administration analysis both.');
insert into instructions (step_no, step_description) values ( '3', 'Bank lot natural low difference east cup.');
insert into instructions (step_no, step_description) values ( '4', 'Action site discover standard teach.');
insert into instructions (step_no, step_description) values ( '1', 'Along beat hair show reason hard.');
insert into instructions (step_no, step_description) values ( '2', 'Another prepare itself try voice bag party.');
insert into instructions (step_no, step_description) values ( '1', 'Time policy development base human though.');
insert into instructions (step_no, step_description) values ( '2', 'Front least cause possible.');
insert into instructions (step_no, step_description) values ( '1', 'Commercial left Mrs major left.');
insert into instructions (step_no, step_description) values ( '2', 'Wish star debate himself help measure.');
insert into instructions (step_no, step_description) values ( '3', 'Civil offer answer.');
insert into instructions (step_no, step_description) values ( '4', 'Note strategy effect. Method item effort side.');
insert into instructions (step_no, step_description) values ( '5', 'Computer single represent ago.');
insert into instructions (step_no, step_description) values ( '6', 'People station by since fish blue.');
insert into instructions (step_no, step_description) values ( '7', 'Reflect policy top score recent ago have.');
insert into instructions (step_no, step_description) values ( '1', 'Either face reduce sister stuff.');
insert into instructions (step_no, step_description) values ( '2', 'Fire so police sing health.');
insert into instructions (step_no, step_description) values ( '3', 'Ground claim leg financial. Study read century.');
insert into instructions (step_no, step_description) values ( '4', 'Team check might top.');
insert into instructions (step_no, step_description) values ( '1', 'Customer Congress under one yes coach.');
insert into instructions (step_no, step_description) values ( '2', 'Letter share day gun over.');
insert into instructions (step_no, step_description) values ( '3', 'Hear once than police.');
insert into instructions (step_no, step_description) values ( '4', 'Rock upon job professor stock design.');
insert into instructions (step_no, step_description) values ( '5', 'Statement police along too eat.');
insert into instructions (step_no, step_description) values ( '6', 'Process television suffer into write.');
insert into instructions (step_no, step_description) values ( '7', 'Understand edge learn record reason.');
insert into instructions (step_no, step_description) values ( '1', 'Collection democratic require contain seven part.');
insert into instructions (step_no, step_description) values ( '2', 'Her deal threat recent economy reduce economic.');
insert into instructions (step_no, step_description) values ( '3', 'While nor film open born important.');
insert into instructions (step_no, step_description) values ( '4', 'Church mention natural sure.');
insert into instructions (step_no, step_description) values ( '1', 'Small strategy language its.');
insert into instructions (step_no, step_description) values ( '2', 'A kid find see money tell.');
insert into instructions (step_no, step_description) values ( '3', 'Bank drop garden prevent discover.');
insert into instructions (step_no, step_description) values ( '4', 'Though east often past history.');
insert into instructions (step_no, step_description) values ( '5', 'Affect measure former total stop state pull.');
insert into instructions (step_no, step_description) values ( '6', 'Unit through community coach cup individual.');

-- Insert measured in data

insert into measured_in (ingredient_id, measurement_id) values ( '1', '9');
insert into measured_in (ingredient_id, measurement_id) values ( '2', '2');
insert into measured_in (ingredient_id, measurement_id) values ( '3', '8');
insert into measured_in (ingredient_id, measurement_id) values ( '4', '7');
insert into measured_in (ingredient_id, measurement_id) values ( '5', '10');
insert into measured_in (ingredient_id, measurement_id) values ( '6', '8');
insert into measured_in (ingredient_id, measurement_id) values ( '7', '7');
insert into measured_in (ingredient_id, measurement_id) values ( '8', '8');
insert into measured_in (ingredient_id, measurement_id) values ( '9', '5');
insert into measured_in (ingredient_id, measurement_id) values ( '10', '8');
insert into measured_in (ingredient_id, measurement_id) values ( '11', '5');
insert into measured_in (ingredient_id, measurement_id) values ( '12', '2');
insert into measured_in (ingredient_id, measurement_id) values ( '13', '10');
insert into measured_in (ingredient_id, measurement_id) values ( '14', '3');
insert into measured_in (ingredient_id, measurement_id) values ( '15', '3');
insert into measured_in (ingredient_id, measurement_id) values ( '16', '10');
insert into measured_in (ingredient_id, measurement_id) values ( '17', '3');
insert into measured_in (ingredient_id, measurement_id) values ( '18', '3');
insert into measured_in (ingredient_id, measurement_id) values ( '19', '8');
insert into measured_in (ingredient_id, measurement_id) values ( '20', '10');

-- Insert stores data

insert into stores (user_id, ingredient_id, quantity) values ( '1', '11','1');
insert into stores (user_id, ingredient_id, quantity) values ( '1', '14','2');
insert into stores (user_id, ingredient_id, quantity) values ( '1', '15','1');
insert into stores (user_id, ingredient_id, quantity) values ( '1', '18','7');
insert into stores (user_id, ingredient_id, quantity) values ( '1', '1','3');
insert into stores (user_id, ingredient_id, quantity) values ( '1', '10','2');
insert into stores (user_id, ingredient_id, quantity) values ( '1', '12','7');
insert into stores (user_id, ingredient_id, quantity) values ( '1', '16','8');
insert into stores (user_id, ingredient_id, quantity) values ( '2', '1','1');
insert into stores (user_id, ingredient_id, quantity) values ( '2', '5','2');
insert into stores (user_id, ingredient_id, quantity) values ( '2', '8','4');
insert into stores (user_id, ingredient_id, quantity) values ( '2', '19','7');
insert into stores (user_id, ingredient_id, quantity) values ( '2', '4','2');
insert into stores (user_id, ingredient_id, quantity) values ( '2', '3','7');
insert into stores (user_id, ingredient_id, quantity) values ( '2', '12','3');
insert into stores (user_id, ingredient_id, quantity) values ( '2', '18','2');
insert into stores (user_id, ingredient_id, quantity) values ( '3', '18','6');
insert into stores (user_id, ingredient_id, quantity) values ( '3', '12','6');
insert into stores (user_id, ingredient_id, quantity) values ( '3', '13','9');
insert into stores (user_id, ingredient_id, quantity) values ( '3', '4','1');
insert into stores (user_id, ingredient_id, quantity) values ( '3', '16','3');
insert into stores (user_id, ingredient_id, quantity) values ( '3', '5','1');
insert into stores (user_id, ingredient_id, quantity) values ( '3', '11','2');
insert into stores (user_id, ingredient_id, quantity) values ( '3', '7','6');
insert into stores (user_id, ingredient_id, quantity) values ( '4', '14','6');
insert into stores (user_id, ingredient_id, quantity) values ( '4', '16','4');
insert into stores (user_id, ingredient_id, quantity) values ( '4', '3','6');
insert into stores (user_id, ingredient_id, quantity) values ( '4', '17','9');
insert into stores (user_id, ingredient_id, quantity) values ( '4', '18','5');
insert into stores (user_id, ingredient_id, quantity) values ( '4', '2','7');
insert into stores (user_id, ingredient_id, quantity) values ( '4', '10','7');
insert into stores (user_id, ingredient_id, quantity) values ( '4', '11','9');
insert into stores (user_id, ingredient_id, quantity) values ( '5', '18','6');
insert into stores (user_id, ingredient_id, quantity) values ( '5', '20','2');
insert into stores (user_id, ingredient_id, quantity) values ( '5', '19','9');
insert into stores (user_id, ingredient_id, quantity) values ( '5', '2','5');
insert into stores (user_id, ingredient_id, quantity) values ( '5', '7','8');
insert into stores (user_id, ingredient_id, quantity) values ( '5', '10','2');
insert into stores (user_id, ingredient_id, quantity) values ( '5', '14','7');
insert into stores (user_id, ingredient_id, quantity) values ( '5', '17','2');

-- Insert made of data

insert into made_of (recipe_id, ingredient_id, amount) values ( '1', '18', '3');
insert into made_of (recipe_id, ingredient_id, amount) values ( '1', '5', '9');
insert into made_of (recipe_id, ingredient_id, amount) values ( '1', '6', '3');
insert into made_of (recipe_id, ingredient_id, amount) values ( '1', '13', '5');
insert into made_of (recipe_id, ingredient_id, amount) values ( '1', '10', '8');
insert into made_of (recipe_id, ingredient_id, amount) values ( '1', '4', '2');
insert into made_of (recipe_id, ingredient_id, amount) values ( '1', '3', '9');
insert into made_of (recipe_id, ingredient_id, amount) values ( '1', '7', '7');
insert into made_of (recipe_id, ingredient_id, amount) values ( '2', '16', '1');
insert into made_of (recipe_id, ingredient_id, amount) values ( '2', '10', '1');
insert into made_of (recipe_id, ingredient_id, amount) values ( '2', '1', '6');
insert into made_of (recipe_id, ingredient_id, amount) values ( '2', '4', '6');
insert into made_of (recipe_id, ingredient_id, amount) values ( '2', '7', '3');
insert into made_of (recipe_id, ingredient_id, amount) values ( '2', '3', '3');
insert into made_of (recipe_id, ingredient_id, amount) values ( '2', '13', '1');
insert into made_of (recipe_id, ingredient_id, amount) values ( '2', '19', '7');
insert into made_of (recipe_id, ingredient_id, amount) values ( '3', '18', '9');
insert into made_of (recipe_id, ingredient_id, amount) values ( '3', '1', '3');
insert into made_of (recipe_id, ingredient_id, amount) values ( '3', '14', '1');
insert into made_of (recipe_id, ingredient_id, amount) values ( '3', '12', '4');
insert into made_of (recipe_id, ingredient_id, amount) values ( '3', '3', '6');
insert into made_of (recipe_id, ingredient_id, amount) values ( '3', '9', '2');
insert into made_of (recipe_id, ingredient_id, amount) values ( '3', '7', '5');
insert into made_of (recipe_id, ingredient_id, amount) values ( '3', '16', '2');
insert into made_of (recipe_id, ingredient_id, amount) values ( '4', '17', '9');
insert into made_of (recipe_id, ingredient_id, amount) values ( '4', '1', '2');
insert into made_of (recipe_id, ingredient_id, amount) values ( '4', '6', '5');
insert into made_of (recipe_id, ingredient_id, amount) values ( '4', '12', '8');
insert into made_of (recipe_id, ingredient_id, amount) values ( '4', '4', '9');
insert into made_of (recipe_id, ingredient_id, amount) values ( '4', '8', '8');
insert into made_of (recipe_id, ingredient_id, amount) values ( '4', '20', '1');
insert into made_of (recipe_id, ingredient_id, amount) values ( '4', '19', '4');
insert into made_of (recipe_id, ingredient_id, amount) values ( '5', '20', '7');
insert into made_of (recipe_id, ingredient_id, amount) values ( '5', '12', '8');
insert into made_of (recipe_id, ingredient_id, amount) values ( '5', '1', '5');
insert into made_of (recipe_id, ingredient_id, amount) values ( '5', '13', '3');
insert into made_of (recipe_id, ingredient_id, amount) values ( '5', '14', '3');
insert into made_of (recipe_id, ingredient_id, amount) values ( '5', '17', '4');
insert into made_of (recipe_id, ingredient_id, amount) values ( '5', '15', '9');
insert into made_of (recipe_id, ingredient_id, amount) values ( '5', '16', '1');
insert into made_of (recipe_id, ingredient_id, amount) values ( '6', '13', '5');
insert into made_of (recipe_id, ingredient_id, amount) values ( '6', '9', '4');
insert into made_of (recipe_id, ingredient_id, amount) values ( '6', '3', '6');
insert into made_of (recipe_id, ingredient_id, amount) values ( '6', '8', '1');
insert into made_of (recipe_id, ingredient_id, amount) values ( '6', '6', '7');
insert into made_of (recipe_id, ingredient_id, amount) values ( '6', '19', '2');
insert into made_of (recipe_id, ingredient_id, amount) values ( '6', '14', '8');
insert into made_of (recipe_id, ingredient_id, amount) values ( '6', '5', '9');
insert into made_of (recipe_id, ingredient_id, amount) values ( '7', '11', '3');
insert into made_of (recipe_id, ingredient_id, amount) values ( '7', '9', '5');
insert into made_of (recipe_id, ingredient_id, amount) values ( '7', '14', '7');
insert into made_of (recipe_id, ingredient_id, amount) values ( '7', '18', '4');
insert into made_of (recipe_id, ingredient_id, amount) values ( '7', '7', '6');
insert into made_of (recipe_id, ingredient_id, amount) values ( '7', '3', '4');
insert into made_of (recipe_id, ingredient_id, amount) values ( '7', '2', '5');
insert into made_of (recipe_id, ingredient_id, amount) values ( '7', '17', '8');
insert into made_of (recipe_id, ingredient_id, amount) values ( '8', '11', '3');
insert into made_of (recipe_id, ingredient_id, amount) values ( '8', '19', '7');
insert into made_of (recipe_id, ingredient_id, amount) values ( '8', '20', '6');
insert into made_of (recipe_id, ingredient_id, amount) values ( '8', '16', '4');
insert into made_of (recipe_id, ingredient_id, amount) values ( '8', '13', '4');
insert into made_of (recipe_id, ingredient_id, amount) values ( '8', '9', '7');
insert into made_of (recipe_id, ingredient_id, amount) values ( '8', '18', '5');
insert into made_of (recipe_id, ingredient_id, amount) values ( '8', '5', '4');
insert into made_of (recipe_id, ingredient_id, amount) values ( '9', '12', '6');
insert into made_of (recipe_id, ingredient_id, amount) values ( '9', '14', '9');
insert into made_of (recipe_id, ingredient_id, amount) values ( '9', '13', '8');
insert into made_of (recipe_id, ingredient_id, amount) values ( '9', '4', '8');
insert into made_of (recipe_id, ingredient_id, amount) values ( '9', '15', '6');
insert into made_of (recipe_id, ingredient_id, amount) values ( '9', '5', '2');
insert into made_of (recipe_id, ingredient_id, amount) values ( '9', '1', '9');
insert into made_of (recipe_id, ingredient_id, amount) values ( '9', '19', '6');
insert into made_of (recipe_id, ingredient_id, amount) values ( '10', '7', '7');
insert into made_of (recipe_id, ingredient_id, amount) values ( '10', '20', '9');
insert into made_of (recipe_id, ingredient_id, amount) values ( '10', '16', '1');
insert into made_of (recipe_id, ingredient_id, amount) values ( '10', '8', '1');
insert into made_of (recipe_id, ingredient_id, amount) values ( '10', '13', '8');
insert into made_of (recipe_id, ingredient_id, amount) values ( '10', '2', '5');
insert into made_of (recipe_id, ingredient_id, amount) values ( '10', '14', '5');
insert into made_of (recipe_id, ingredient_id, amount) values ( '10', '4', '7');

-- Insert prepare data

insert into prepare (recipe_id, instruction_id, step_no) values ( '1', '1', '1');
insert into prepare (recipe_id, instruction_id, step_no) values ( '1', '2', '2');
insert into prepare (recipe_id, instruction_id, step_no) values ( '1', '3', '3');
insert into prepare (recipe_id, instruction_id, step_no) values ( '1', '4', '4');
insert into prepare (recipe_id, instruction_id, step_no) values ( '2', '5', '1');
insert into prepare (recipe_id, instruction_id, step_no) values ( '2', '6', '2');
insert into prepare (recipe_id, instruction_id, step_no) values ( '2', '7', '3');
insert into prepare (recipe_id, instruction_id, step_no) values ( '2', '8', '4');
insert into prepare (recipe_id, instruction_id, step_no) values ( '2', '9', '5');
insert into prepare (recipe_id, instruction_id, step_no) values ( '3', '10', '1');
insert into prepare (recipe_id, instruction_id, step_no) values ( '3', '11', '2');
insert into prepare (recipe_id, instruction_id, step_no) values ( '3', '12', '3');
insert into prepare (recipe_id, instruction_id, step_no) values ( '3', '13', '4');
insert into prepare (recipe_id, instruction_id, step_no) values ( '4', '14', '1');
insert into prepare (recipe_id, instruction_id, step_no) values ( '4', '15', '2');
insert into prepare (recipe_id, instruction_id, step_no) values ( '5', '16', '1');
insert into prepare (recipe_id, instruction_id, step_no) values ( '5', '17', '2');
insert into prepare (recipe_id, instruction_id, step_no) values ( '6', '18', '1');
insert into prepare (recipe_id, instruction_id, step_no) values ( '6', '19', '2');
insert into prepare (recipe_id, instruction_id, step_no) values ( '6', '20', '3');
insert into prepare (recipe_id, instruction_id, step_no) values ( '6', '21', '4');
insert into prepare (recipe_id, instruction_id, step_no) values ( '6', '22', '5');
insert into prepare (recipe_id, instruction_id, step_no) values ( '6', '23', '6');
insert into prepare (recipe_id, instruction_id, step_no) values ( '6', '24', '7');
insert into prepare (recipe_id, instruction_id, step_no) values ( '7', '25', '1');
insert into prepare (recipe_id, instruction_id, step_no) values ( '7', '26', '2');
insert into prepare (recipe_id, instruction_id, step_no) values ( '7', '27', '3');
insert into prepare (recipe_id, instruction_id, step_no) values ( '7', '28', '4');
insert into prepare (recipe_id, instruction_id, step_no) values ( '8', '29', '1');
insert into prepare (recipe_id, instruction_id, step_no) values ( '8', '30', '2');
insert into prepare (recipe_id, instruction_id, step_no) values ( '8', '31', '3');
insert into prepare (recipe_id, instruction_id, step_no) values ( '8', '32', '4');
insert into prepare (recipe_id, instruction_id, step_no) values ( '8', '33', '5');
insert into prepare (recipe_id, instruction_id, step_no) values ( '8', '34', '6');
insert into prepare (recipe_id, instruction_id, step_no) values ( '8', '35', '7');
insert into prepare (recipe_id, instruction_id, step_no) values ( '9', '36', '1');
insert into prepare (recipe_id, instruction_id, step_no) values ( '9', '37', '2');
insert into prepare (recipe_id, instruction_id, step_no) values ( '9', '38', '3');
insert into prepare (recipe_id, instruction_id, step_no) values ( '9', '39', '4');
insert into prepare (recipe_id, instruction_id, step_no) values ( '10', '40', '1');
insert into prepare (recipe_id, instruction_id, step_no) values ( '10', '41', '2');
insert into prepare (recipe_id, instruction_id, step_no) values ( '10', '42', '3');
insert into prepare (recipe_id, instruction_id, step_no) values ( '10', '43', '4');
insert into prepare (recipe_id, instruction_id, step_no) values ( '10', '44', '5');
insert into prepare (recipe_id, instruction_id, step_no) values ( '10', '45', '6');

-- Insert created data

insert into creates (user_id, recipe_id) values ( '1', '1');
insert into creates (user_id, recipe_id) values ( '2', '2');
insert into creates (user_id, recipe_id) values ( '3', '3');
insert into creates (user_id, recipe_id) values ( '4', '4');
insert into creates (user_id, recipe_id) values ( '4', '5');
insert into creates (user_id, recipe_id) values ( '5', '6');
insert into creates (user_id, recipe_id) values ( '5', '7');
insert into creates (user_id, recipe_id) values ( '5', '8');
insert into creates (user_id, recipe_id) values ( '5', '9');
insert into creates (user_id, recipe_id) values ( '5', '10');
