"""Views for users"""
import os
import datetime

from flask import jsonify, request
from flask_restful import Resource
from app.api.token_decorator import require_token
from app.api.validators import only_admin_can_edit
import jwt
from .models import UserModel

secret = os.getenv("SECRET_KEY")


def nonexistent_user():
    return jsonify({"status": 404, "message": "user does not exist"})


def admin_user():
    return jsonify({"status": 403, "message": "Only admin can access this route"})


class UserSignUp(Resource):
    """Class with user signup post method"""

    def __init__(self):
        self.db = UserModel()

    def post(self):
        """method to post user details"""
        user = self.db.save()

        if user == "email already exists":
            return jsonify({"status": 400, "error": "email already exists"})
        payload = {
            "email": user["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        }
        token = jwt.encode(payload=payload, key=secret, algorithm="HS256")

        user_details = {
            "name": user["first_name"] + " " + user["last_name"],
            "email": user["email"],
            "admission_number": user["admission_number"],
        }
        return jsonify(
            {
                "status": 201,
                "data": [
                    {
                        "account details": user_details,
                        "token": token,
                        "message": "You have created a new account",
                    }
                ],
            }
        )


class UserSignIn(Resource):
    """Class containing user login method"""

    def __init__(self):
        self.db = UserModel()

    def post(self):
        """method to get a specific user"""
        user = self.db.log_in()
        if user is None:
            return nonexistent_user()

        if user == "incorrect password":
            return jsonify(
                {
                    "status": 401,
                    "message": "password or email is incorrect please try again",
                }
            )

        payload = {
            "email": user,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        }
        token = jwt.encode(payload=payload, key=secret, algorithm="HS256")

        return jsonify(
            {
                "status": 200,
                "data": [
                    {
                        "token": token,
                        "user": user,
                        "message": "You are now signed in",
                    }
                ],
            }
        )


class Users(Resource):
    """Class with methods for dealing with all users"""

    def __init__(self):
        self.db = UserModel()

    @require_token
    def get(current_user, self):
        """method to get all users"""
        if current_user["isadmin"] is False:
            return admin_user()

        return jsonify({"status": 200, "data": self.db.find_users()})


class Search(Resource):
    """docstring filtering users by admission_number"""

    def __init__(self):
        """initiliase the user class"""
        self.db = UserModel()

    @require_token
    def get(current_user, self, admission_number):
        """method for getting a specific user by admission_number"""
        if current_user["isadmin"] is False:
            return admin_user()

        user = self.db.find_user_by_admin_num(admission_number)
        if user is None:
            return nonexistent_user()

        user_details = {
            "name": user["first_name"] + " " + user["last_name"],
            "email": user["email"],
            "admission_number": user["admission_number"],
            "registered": user["registered"],
            "isAdmin": user["isadmin"],
        }
        return jsonify({"status": 200, "data": user_details})

    @require_token
    def delete(current_user, self, admission_number):
        """method to delete a user"""

        user = self.db.find_user_by_admin_num(admission_number)
        if user is None:
            return nonexistent_user()

        if current_user["isadmin"] is not True:
            return jsonify(
                {"status": 403, "message": "Only an admin can delete a user"}
            )

        delete_status = self.db.delete_user(user["email"])
        if delete_status is True:

            return jsonify({"status": 200, "message": "user record has been deleted"})


class UserAdminStatus(Resource):
    """Class with method for updating a  specific user admin status"""

    def __init__(self):
        self.db = UserModel()

    @require_token
    def patch(current_user, self, admission_number):
        """method to promote a user"""
        user = self.db.find_user_by_admin_num(admission_number)
        if user is None:
            return nonexistent_user()

        if current_user["isadmin"] is not True:
            return jsonify(
                {
                    "status": 403,
                    "message": "Only an admin can change the status of a user",
                }
            )

        user_status_updated = self.db.edit_user_status(user["email"])
        if user_status_updated is True:
            success_message = {
                "admission number": user["admission_number"],
                "message": "User status has been updated",
            }
            return jsonify({"status": 200, "data": success_message})
