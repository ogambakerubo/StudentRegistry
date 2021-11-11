"""Courses Models"""
import datetime
from flask import request
from flask_restful import reqparse
from app.db_con import connection
from app.db_con import DATABASE_URL as url
import re
import psycopg2.extras
from ..validators import (
    parser_course,
    parser_edit_course,
)


class CoursesModel:
    """Class with methods to perform CRUD operations on the DB"""

    def __init__(self):
        self.db = connection(url)

    def save(self, users_id):
        parser_course.parse_args()
        data = {
            "created_on": datetime.datetime.utcnow(),
            "created_by": users_id,
            "course_name": request.json.get("course_name"),
            "course_code": request.json.get("course_code"),
            "year_offered": request.json.get("year_offered"),
        }

        course = self.find_course_by_name_code(data["course_name"], data["course_code"])
        if course != "Course entry does not exist":
            return "Course name or code already exists"

        query = """INSERT INTO courses (created_on,created_by,course_name,course_code,year_offered) VALUES('{0}',{1},'{2}','{3}','{4}');""".format(
            data["created_on"],
            data["created_by"],
            data["course_name"],
            data["course_code"],
            data["year_offered"],
        )
        con = self.db
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()

        return data

    def find_course_entry_by_code(self, course_code):
        """method to find a course entry"""
        query = """SELECT * from courses WHERE course_code='{0}' ;""".format(
            course_code
        )
        con = self.db
        cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        course = cursor.fetchone()
        if cursor.rowcount == 0:
            return "Course entry does not exist"

        return course

    def find_course_by_name_code(self, course_name, course_code):
        """method to find a course entry"""
        query = """SELECT * from courses WHERE (course_name='{0}') OR (course_code='{1}') ;""".format(
            course_name, course_code
        )
        con = self.db
        cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        course = cursor.fetchone()
        if cursor.rowcount == 0:
            return "Course entry does not exist"

        return course

    def edit_course(self, course_code):
        "Method to edit a single course entry"
        parser_edit_course.parse_args()
        new_course_name = request.json.get("course_name")
        new_course_code = request.json.get("course_code")
        new_year_offered = request.json.get("year_offered")

        if self.find_course_entry_by_code(course_code) == "Course entry does not exist":
            return "Course entry does not exist"

        course = self.find_course_by_name_code(new_course_name, new_course_code)
        if course != "Course entry does not exist":
            return "Course name or code already exists"

        course = self.grades_constraints(course_code)
        if course is not None:
            return course

        query = """UPDATE courses SET course_name='{0}', course_code='{1}', year_offered='{2}' WHERE course_code='{3}';""".format(
            new_course_name, new_course_code, new_year_offered, course_code
        )
        con = self.db
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()

        return "Course updated"

    def grades_constraints(self, course_code):
        """Method to check if a course entry is in use"""
        course = self.find_course_entry_by_code(course_code)
        if course == "Course entry does not exist":
            return None

        query = """SELECT * FROM grades WHERE course_code='{0}';""".format(course_code)
        con = self.db
        cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        course = cursor.fetchone()
        if cursor.rowcount == 0:
            return None

        return "Course entry cannot be updated or deleted"

    def delete(self, course_code):
        """Method to delete a single course entry"""
        course = self.find_course_entry_by_code(course_code)
        if course == "Course entry does not exist":
            return None

        course = self.grades_constraints(course_code)
        if course is not None:
            return course

        query = """DELETE FROM courses WHERE course_code='{0}';""".format(course_code)
        con = self.db
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()

        return "Course entry deleted"
