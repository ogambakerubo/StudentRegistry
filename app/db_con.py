"""driver for interacting with PostgreSQL from the Python scripting language"""
import os

import psycopg2 as psy
import psycopg2.extras
from werkzeug.security import generate_password_hash


ENV = os.getenv("FLASK_ENV")
DATABASE_URL = os.getenv("DATABASE_URL")
SUPER_USER_PASSWORD = os.getenv("SUPER_USER_PASSWORD")


if ENV == "testing":
    DATABASE_URL = os.getenv("DATABASE_URL_TEST")


def connection(url):
    con = psy.connect(DATABASE_URL)

    return con


def create_tables():
    """
    A database cursor is an object that points to a
    place in the database where we want to create, read,
    update, or delete data.
    """
    con = connection(DATABASE_URL)
    curr = con.cursor()
    queries = tables()

    try:
        for query in queries:
            curr.execute(query)
        con.commit()
        print("Creating tables ... Done!")
    except:
        print("Failed to create tables")


def destroy_tables():
    con = connection(DATABASE_URL)
    curr = con.cursor()
    users = "DROP TABLE IF EXISTS users CASCADE;"
    courses = "DROP TABLE IF EXISTS courses CASCADE;"
    grades = "DROP TABLE IF EXISTS grades CASCADE;"
    queries = [courses, users, grades]

    try:
        for query in queries:
            curr.execute(query)
        con.commit()
        print("Destroying test tables...Done")
    except:
        print("Failed to Destroy tables")


def tables():
    tbl1 = """CREATE TABLE IF NOT EXISTS courses (
	    courses_id serial PRIMARY KEY NOT NULL,
        created_on TIMESTAMP,
	    course_name varchar(64) NOT NULL UNIQUE,
	    course_code varchar(50) NOT NULL UNIQUE,
        year_offered integer NOT NULL,
        created_by serial NOT NULL
	    );"""

    tbl2 = """CREATE TABLE IF NOT EXISTS users (
     users_id serial PRIMARY KEY NOT NULL,
     first_name character(50) NOT NULL,
     last_name character(50),
     email varchar(50) NOT NULL UNIQUE,
     admission_number varchar(50) NOT NULL UNIQUE,
     isAdmin boolean NOT NULL,  
     registered TIMESTAMP, 
     password varchar(500) NOT NULL
     );"""

    tbl3 = """CREATE TABLE IF NOT EXISTS grades (
     grades_id serial PRIMARY KEY NOT NULL,
     users_id serial REFERENCES users(users_id),
     course_name varchar(64) REFERENCES courses(course_name),
     course_code varchar(50) REFERENCES courses(course_code),
     grade varchar(50),
     marks_scored integer NOT NULL,
     admission_number varchar(50) REFERENCES users(admission_number),
     registered TIMESTAMP 
     );"""

    queries = [tbl1, tbl2, tbl3]

    return queries


def super_user():
    password = generate_password_hash(SUPER_USER_PASSWORD)
    user_admin = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.org",
        "admission_number": "ADMIN-0001-2021",
        "isAdmin": True,
        "registered": "Thu, 15 Jul 2021 21:00:00 GMT",
        "password": password,
    }

    query = """INSERT INTO users (first_name,last_name,email,admission_number,password,isAdmin,registered) VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}');""".format(
        user_admin["first_name"],
        user_admin["last_name"],
        user_admin["email"],
        user_admin["admission_number"],
        user_admin["password"],
        user_admin["isAdmin"],
        user_admin["registered"],
    )

    conn = connection(DATABASE_URL)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        conn.commit()
        print("Super user created")
    except:
        print("User already exists")
