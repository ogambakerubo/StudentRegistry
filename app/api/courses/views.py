"""Views for Courses"""
from flask import jsonify, make_response, request
from flask_restful import Resource

from app.api.users.models import UserModel

from ..validators import (
    non_existent_entry,
    only_admin_can_edit,
)
from .models import CoursesModel
from app.api.token_decorator import require_token


class Course(Resource):
    """docstring for a single Course class"""

    def __init__(self):
        """initiliase the Courses class"""
        self.db = CoursesModel()

    @require_token
    def post(current_user, self):
        """method for saving a course"""
        if current_user["isadmin"] is False:
            return only_admin_can_edit()

        course = self.db.save(current_user["users_id"])
        if course == "Course entry cannot be updated or deleted":
            return jsonify(
                {
                    "status": 400,
                    "message": course,
                }
            )

        return jsonify(
            {
                "status": 201,
                "message": "Created a new course entry",
                "data": course,
            }
        )


class SingleCourse(Resource):
    """docstring for a single Course class"""

    def __init__(self):
        """initiliase the Courses class"""
        self.db = CoursesModel()

    @require_token
    def get(current_user, self, course_code):
        """method for getting a single course by courses_id"""

        course = self.db.find_course_entry_by_code(course_code)

        if course == "Course entry does not exist":
            return non_existent_entry()

        return jsonify({"status": 200, "data": course})

    @require_token
    def patch(current_user, self, course_code):
        """method for updating a single course by courses_id"""
        if current_user["isadmin"] is False:
            return only_admin_can_edit()

        course = self.db.edit_course(course_code)

        if course == "Course entry does not exist":
            return non_existent_entry()

        if course == "Course name or code already exists":
            return jsonify(
                {
                    "status": 400,
                    "message": course,
                }
            )

        if course == "Course entry cannot be updated or deleted":
            return jsonify(
                {
                    "status": 400,
                    "message": course,
                }
            )

        return jsonify(
            {"status": 200, "message": "Course record updated", "data": course}
        )

    @require_token
    def delete(current_user, self, course_code):
        """method for deleting a single course by courses_id"""
        if current_user["isadmin"] is False:
            return only_admin_can_edit()

        course = self.db.delete(course_code)

        if course == None:
            return non_existent_entry()

        if course == "Course entry cannot be updated or deleted":
            return jsonify(
                {
                    "status": 400,
                    "message": course,
                }
            )

        return jsonify({"status": 200, "message": "Course record has been deleted"})
