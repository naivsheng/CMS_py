CREATE DATABASE cms_db;
use cms_db;

CREATE TABLE users (
  id INT(11) NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE reminders (
  id INT(11) NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  reminder_text VARCHAR(255) NOT NULL,
  reminder_date DATE NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE communications (
  id INT(11) NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  communication_text VARCHAR(255) NOT NULL,
  communication_date DATE NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE tasks (
  user_id INT(11) NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  Executors Varchar(50) not null,
  task_titel Varchar(20) not null,
  task_detail VARCHAR(255) NOT NULL,
  create_date DATE NOT NULL,
  end_date Date,
  PRIMARY KEY (id)
);
use cms_db;
#show tables;
select * from users;
