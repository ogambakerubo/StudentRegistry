"""Views for Grades"""
from flask import jsonify, make_response, request
from flask_restful import Resource

from app.api.users.models import UserModel

from ..validators import (
    non_existent_entry,
    only_admin_can_edit,
)
from .models import GradesModel
from app.api.token_decorator import require_token


class Grades(Resource):
    """docstring for a single Grade class"""

    def __init__(self):
        """initiliase the Grades class"""
        self.db = GradesModel()

    @require_token
    def post(current_user, self):
        """method for saving a grade"""
        if current_user["isadmin"] is False:
            return only_admin_can_edit()

        grade = self.db.save(current_user["users_id"])
        if grade == "Record already exists":
            return jsonify(
                {
                    "status": 400,
                    "message": grade,
                }
            )

        return jsonify(
            {
                "status": 201,
                "message": "Created a new grade entry",
                "data": grade,
            }
        )


class SingleGrade(Resource):
    """docstring for a single Grade class"""

    def __init__(self):
        """initiliase the Grades class"""
        self.db = GradesModel()

    @require_token
    def get(current_user, self, course_code, admission_number):
        """method for getting a single grade by grades_id"""
        if current_user["isadmin"] is False:
            return only_admin_can_edit()

        grade = self.db.find_grade_entry(course_code, admission_number)

        if grade == "grade entry does not exist":
            return non_existent_entry()

        return jsonify({"status": 200, "data": grade})

    @require_token
    def patch(current_user, self, course_code, admission_number):
        """method for updating a single grade by grades_id"""
        if current_user["isadmin"] is False:
            return only_admin_can_edit()

        grade = self.db.edit_grade(course_code, admission_number)

        if grade != "grades updated":
            return non_existent_entry()

        return jsonify(
            {"status": 200, "message": "Grade record updated", "data": grade}
        )

    @require_token
    def delete(current_user, self, course_code, admission_number):
        """method for deleting a single grade by grades_id"""
        if current_user["isadmin"] is False:
            return only_admin_can_edit()

        grade = self.db.delete(course_code, admission_number)

        if grade != "Grade entry deleted":
            return non_existent_entry()

        return jsonify({"status": 200, "message": "grade record has been deleted"})


class GradesByCourseCode(Resource):
    """docstring for retrieving Grades by course code class"""

    def __init__(self):
        """initiliase the Grades class"""
        self.db = GradesModel()

    @require_token
    def get(current_user, self, course_code):
        """method for getting all the grades in a certain course"""
        if current_user["isadmin"] is False:
            return only_admin_can_edit()

        grade = self.db.find_course_grade(course_code)

        if grade == "grade entries do not exist":
            return non_existent_entry()

        return jsonify({"status": 200, "data": grade})


class AllGradesByAdminNum(Resource):
    """docstring for retrieving all Grades by a single student"""

    def __init__(self):
        """initiliase the Grades class"""
        self.db = GradesModel()

    @require_token
    def get(current_user, self, admission_number):
        """method for getting all the grades by a single student"""
        if (
            current_user["admission_number"] == admission_number
            or current_user["isadmin"] is False
        ):
            return only_admin_can_edit()

        grade = self.db.find_all_student_grades(admission_number)

        if grade == "grade entry does not exist":
            return non_existent_entry()

        return jsonify({"status": 200, "data": grade})
