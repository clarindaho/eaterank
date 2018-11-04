--
-- setup file for eaterank project.
--

-- create database and user and grant privileges to user
create database eaterank_project;
create user 'mysql_username'@'localhost' identified by 'mysql_password';
grant all on eaterank_project.* to 'mysql_username'@'localhost';
flush privileges;

-- select the database and create tables
use eaterank_project;
create table crew(
    crew_id int not null auto_increment primary key,
    location varchar(255) not null,
    cuisine_type varchar(255) not null,
    selected_restaurant varchar(255)
);

create table vote(
    vote_id int not null auto_increment primary key,
    crew_id int,
    restaurant_id int,
    vote_num int not null
);

create table restaurant(
    restaurant_id int not null auto_increment primary key,
    cuisine varchar(255),
    address varchar(255),
    phone_num varchar(255),
    rating float,
    price_range varchar(255),
    image varchar(255),
    menu_url varchar(255)
);

create table user(
    user_id int not null auto_increment primary key,
    crew_id int,
    vote_id int
);
