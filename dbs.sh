#!/bin/bash

HOST='localhost'
USER='root'
PASS='root'

mysql -h $HOST -u $USER -p$PASS -e "

CREATE DATABASE IF NOT EXISTS uplytics_db;

USE mysql;
GRANT ALL PRIVILEGES ON uplytics_db TO $USER@$HOST;

USE uplytics_db;

CREATE TABLE IF NOT EXISTS company_list (
	   company_id int primary key,
	   company_name varchar(128),
	   url varchar(128),
	   image_location varchar(128),
	   date_created datetime,
	   date_updated datetime,
	   type_id int
);

CREATE TABLE IF NOT EXISTS company_type (
	   type_id int primary key,
	   type_name varchar(64),
	   type_description text
);

CREATE TABLE IF NOT EXISTS about_companies (
	   about_id int primary key,
	   company_id int,
	   about_url varchar(128),
	   about_page text,
	   date_created datetime,
	   date_last_read datetime
);

CREATE TABLE IF NOT EXISTS company_jobs (
	   job_id int primary key,
	   company_id int,
	   job_title varchar(128),
	   job_description varchar(128),
	   salary varchar(128),
	   city varchar(128),
	   date_posted datetime,
	   date_last_read datetime
);

CREATE TABLE IF NOT EXISTS vc_clients (
	   relationship_id int primary key,
	   vc_id int,
	   company_id int
);

CREATE TABLE IF NOT EXISTS investments (
	   investment_id int primary key,
	   relationship_id int,
	   round varchar(32),
	   investment_amount varchar(128),
	   investment_date datetime,
	   lead tinyint,
	   notes text
);

CREATE TABLE IF NOT EXISTS articles (
	   article_id int primary key,
	   company_id int,
	   url varchar(128),
	   date_read datetime,
	   article_text text,
	   tags text
);

CREATE TABLE IF NOT EXISTS news_mentions (
	   mention_id int primary key,
	   article_id int,
	   company_id int
);"






	   
