"""Grades Models"""
import datetime
from flask import request
from flask_restful import reqparse
from app.db_con import connection
from app.db_con import DATABASE_URL as url
import re
import psycopg2.extras
from ..validators import (
    parser,
    parser_edit_grade,
)


class GradesModel:
    """Class with methods to perform CRUD operations on the DB"""

    def __init__(self):
        self.db = connection(url)

    def save(self, users_id):
        parser.parse_args()
        data = {
            "registered": datetime.datetime.utcnow(),
            "users_id": users_id,
            "course_name": request.json.get("course_name"),
            "course_code": request.json.get("course_code"),
            "grade": request.json.get("grade"),
            "marks_scored": request.json.get("marks_scored"),
            "admission_number": request.json.get("admission_number"),
        }

        grade = self.find_grade_entry(data["course_code"], data["admission_number"])
        if grade != "grade entry does not exist":
            return "Record already exists"

        query = """INSERT INTO grades (registered,users_id,course_name,course_code,grade,marks_scored,admission_number) VALUES('{0}',{1},'{2}','{3}','{4}','{5}','{6}');""".format(
            data["registered"],
            data["users_id"],
            data["course_name"],
            data["course_code"],
            data["grade"],
            data["marks_scored"],
            data["admission_number"],
        )
        con = self.db
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()

        return data

    def find_grade_entry(self, course_code, admission_number):
        """method to find a students grades entry"""
        query = """SELECT * from grades WHERE (course_code='{0}') AND (admission_number='{1}') ;""".format(
            course_code, admission_number
        )
        con = self.db
        cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        grade = cursor.fetchone()
        if cursor.rowcount == 0:
            return "grade entry does not exist"

        return grade

    def find_course_grade(self, course_code):
        """method to find all students grades in a course"""
        query = """SELECT * from grades WHERE  course_code='{0}' ;""".format(
            course_code
        )
        con = self.db
        cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        grade = cursor.fetchall()
        if cursor.rowcount == 0:
            return "grade entries do not exist"

        return grade

    def find_all_student_grades(self, admission_number):
        """method to find all students grades"""
        query = """SELECT * from grades WHERE  admission_number='{0}' ;""".format(
            admission_number
        )
        con = self.db
        cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        grade = cursor.fetchall()
        if cursor.rowcount == 0:
            return "grade entry does not exist"

        return grade

    def edit_grade(self, course_code, admission_number):
        "Method to edit a single grade entry"
        parser_edit_grade.parse_args()
        grade = request.json.get("grade")
        marks_scored = request.json.get("marks_scored")

        if (
            self.find_grade_entry(course_code, admission_number)
            == "grade entry does not exist"
        ):
            return None

        query = """UPDATE grades SET grade='{0}', marks_scored='{1}' WHERE course_code='{2}' AND admission_number='{3}';""".format(
            grade, marks_scored, course_code, admission_number
        )
        con = self.db
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()

        return "grades updated"

    def delete(self, course_code, admission_number):
        "Method to delete a single grade entry"
        grade = self.find_grade_entry(course_code, admission_number)
        if grade is None:
            return None

        query = """DELETE FROM grades WHERE course_code='{0}' AND admission_number='{1}';""".format(
            course_code, admission_number
        )
        con = self.db
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()

        return "Grade entry deleted"
