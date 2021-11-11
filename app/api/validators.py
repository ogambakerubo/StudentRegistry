"""for fields validations purposes"""
import re

from flask import jsonify, request
from flask_restful import reqparse
from werkzeug.utils import validate_arguments

parser = reqparse.RequestParser(bundle_errors=True)
parser_course = reqparse.RequestParser(bundle_errors=True)
parser_edit_course = reqparse.RequestParser(bundle_errors=True)
parser_edit_grade = reqparse.RequestParser(bundle_errors=True)


def validate_integer(value):
    """method to check for only integers"""
    if not re.match(r"^[0-9]+$", value):
        raise ValueError("Pattern not matched")


def validate_string(value):
    """method to check for only letters"""
    if not re.match(r"^[A-Za-z]+$", value):
        raise ValueError("Pattern not matched")


def validate_varchar(value):
    """method to check for only letters, numbers"""
    if not re.match(r"^[ A-Za-z0-9]+$", value):
        raise ValueError("Pattern not matched")


def validate_admission(value):
    """method to check that the field takes only letters, numbers, slashes"""
    if not re.match(r"[A-Za-z0-9/]+", value):
        raise ValueError("Pattern not matched")


def validate_password(value):
    """method to check if password contains more than 8 characters"""
    if not re.match(r"^[A-Za-z0-9!@#$%^&+*=]{8,}$", value):
        raise ValueError("Password should be at least 8 characters")


def validate_email(value):
    """method to check for valid email"""
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", value):
        raise ValueError("Invalid Email")


def non_existent_entry():
    """return message for an entry that does not exist"""
    return jsonify({"status": 404, "error": "entry does not exist"})


def only_admin_can_edit():
    """return message for only an admin can change an entry"""
    return jsonify(
        {
            "status": 403,
            "message": "sorry only an admin can change a entry",
        }
    )


# def only_admin_can_delete():
#     """return message that only admin can delete a this entry"""
#     return jsonify({"status": 401, "error": "sorry you can't delete a this entry"})


# def can_only_edit_draft():
#     """return message that you can patch an incident only on its draft state"""
#     return jsonify({"status": 401, "error": "You can't edit this due to it's state"})


parser.add_argument(
    "marks_scored",
    type=validate_integer,
    required=True,
    trim=True,
    nullable=False,
    help="This field cannot be left blank or should be properly formated",
)

parser.add_argument(
    "admission_number",
    type=validate_admission,
    required=True,
    trim=True,
    nullable=False,
    help="This field cannot be left blank or should be properly formated",
)

parser.add_argument(
    "course_code",
    type=validate_varchar,
    required=True,
    trim=True,
    nullable=False,
    help="This field cannot be left blank or should be properly formated",
)

parser.add_argument(
    "course_name",
    type=validate_varchar,
    required=True,
    trim=True,
    nullable=False,
    help="This field cannot be left blank or should be properly formated",
)

parser.add_argument(
    "grade",
    type=validate_string,
    required=True,
    trim=True,
    nullable=False,
    help="This field cannot be left blank or should be properly formated",
)

parser_course.add_argument(
    "course_name",
    type=validate_varchar,
    required=True,
    trim=True,
    nullable=False,
    help="This field cannot be left blank or should be properly formated",
)

parser_course.add_argument(
    "course_code",
    type=validate_varchar,
    required=True,
    trim=True,
    nullable=False,
    help="This field cannot be left blank or should be properly formated",
)

parser_course.add_argument(
    "year_offered",
    type=validate_integer,
    required=True,
    trim=True,
    nullable=False,
    help="This field cannot be left blank or should be properly formated",
)

parser_edit_course.add_argument(
    "course_name",
    type=validate_varchar,
    required=True,
    trim=True,
    nullable=False,
    help="This field cannot be left blank or should be properly formated",
)

parser_edit_course.add_argument(
    "course_code",
    type=validate_varchar,
    required=True,
    trim=True,
    nullable=False,
    help="This field cannot be left blank or should be properly formated",
)

parser_edit_course.add_argument(
    "year_offered",
    type=validate_integer,
    required=True,
    trim=True,
    nullable=False,
    help="This field cannot be left blank or should be properly formated",
)


parser_edit_grade.add_argument(
    "grade",
    type=validate_string,
    required=True,
    trim=True,
    nullable=False,
    help="This field cannot be left blank or should be properly formated",
)

parser_edit_grade.add_argument(
    "marks_scored",
    type=validate_integer,
    required=True,
    trim=True,
    nullable=False,
    help="This field cannot be left blank or should be properly formated",
)
