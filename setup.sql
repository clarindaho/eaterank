--
-- setup file for eaterank project.
--

-- create database and user and grant privileges to user
create database eaterank_project;
create user 'mysql_username'@'localhost' identified with mysql_native_password by 'mysql_password';
grant all on eaterank_project.* to 'mysql_username'@'localhost';
flush privileges;

-- select the database and create tables
use eaterank_project;
create table crew(
    crew_id int not null auto_increment primary key,
    location varchar(255),
    #cuisine_type0 varchar(255),
    #cuisine_type1 varchar(255),
    #cuisine_type2 varchar(255),
    selected_restaurant varchar(255),
    vote_started boolean
);

create table vote(
    vote_id int not null auto_increment primary key,
    crew_id int,
    restaurant_id int,
    vote_num int not null
);

create table restaurant(
    restaurant_id int not null auto_increment primary key,
    name varchar(255),
    cuisine varchar(255),
    address varchar(255),
    rating float,
    price_range varchar(255),
    menu_url varchar(255),
    image_url varchar(255)
);
