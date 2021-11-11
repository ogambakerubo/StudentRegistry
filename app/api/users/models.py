"""model for users view file"""

import datetime

import psycopg2.extras
from flask import request
from flask_restful import reqparse
from werkzeug.security import check_password_hash, generate_password_hash

from app.db_con import connection
from app.db_con import DATABASE_URL as url
from ..validators import (
    validate_email,
    validate_string,
    validate_password,
    validate_admission,
)

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument(
    "first_name",
    type=validate_string,
    required=True,
    nullable=False,
    trim=True,
    help="This field cannot be left blank or should be properly formated",
)

parser.add_argument(
    "last_name",
    type=validate_string,
    required=True,
    nullable=False,
    help="This field cannot be left blank or should be properly formated",
)

parser.add_argument(
    "email",
    type=validate_email,
    required=True,
    nullable=False,
    trim=True,
    help="This field cannot be left blank or should be properly formated",
)

parser.add_argument(
    "admission_number",
    type=validate_admission,
    required=False,
    trim=True,
    nullable=True,
    help="This field cannot be left blank or should be properly formated",
)

parser.add_argument(
    "password",
    type=validate_password,
    required=True,
    nullable=False,
    help="This field cannot be left blank or should be properly formated and should contain atleast 8 characters",
)


class UserModel:
    """class for manipulating user data"""

    def __init__(self):
        self.registered = datetime.datetime.utcnow()
        self.isAdmin = False
        self.db = connection(url)

    def set_pswd(self, password):
        """salting the passwords"""
        return generate_password_hash(password)

    def check_pswd(self, password):
        return check_password_hash(self.pwdhash, password)

    def save(self):
        parser.parse_args()
        data = {
            "first_name": request.json.get("first_name"),
            "last_name": request.json.get("last_name"),
            "email": request.json.get("email"),
            "admission_number": request.json.get("admission_number"),
            "password": self.set_pswd(request.json.get("password")),
            "isAdmin": self.isAdmin,
            "registered": self.registered,
        }

        user_by_email = self.find_user_by_email(data["email"])

        if user_by_email != None:
            return "email already exists"
        query = """INSERT INTO users (first_name,last_name,email,admission_number,password,isAdmin,registered) VALUES('{0}','{1}','{2}','{3}','{4}','{5}', '{6}');""".format(
            data["first_name"],
            data["last_name"],
            data["email"],
            data["admission_number"],
            data["password"],
            data["isAdmin"],
            data["registered"],
        )
        con = self.db
        cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        con.commit()

        return data

    def find_user_by_email(self, email):
        "Method to find a user by email"
        query = """SELECT * from users WHERE email='{0}';""".format(email)
        con = self.db
        cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        row = cursor.fetchone()

        if cursor.rowcount == 0:
            return None

        return row

    def find_user_by_admin_num(self, admission_number):
        "Method to find a user by admission_number"
        query = """SELECT * from users WHERE admission_number='{0}';""".format(
            admission_number
        )
        con = self.db
        cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        row = cursor.fetchone()

        if cursor.rowcount == 0:
            return None

        return row

    def log_in(self):
        data = {
            "email": request.json.get("email"),
            "password": request.json.get("password"),
        }
        user = self.find_user_by_email(data["email"])
        if user == None:
            return None
        if check_password_hash(user["password"], data["password"]) == False:
            return "incorrect password"

        return user["email"]

    def find_users(self):
        """method to find all users"""
        query = """SELECT * from users;"""
        con = self.db
        cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        rows = cursor.fetchall()

        return rows

    def edit_user_status(self, email):
        """method to update a user to an admin user"""
        isAdmin = True
        query = """UPDATE users SET isadmin={0} WHERE email='{1}';""".format(
            isAdmin, email
        )
        con = self.db
        cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        con.commit()

        return True

    def delete_user(self, email):
        """method to delete a user record"""
        query = """DELETE FROM users WHERE email='{0}';""".format(email)
        con = self.db
        cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        con.commit()

        return True
