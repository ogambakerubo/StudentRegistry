"""all api routes"""
from flask import Blueprint
from flask_restful import Api

from .users.views import UserSignUp, UserSignIn, Users, Search, UserAdminStatus
from .grades.views import (
    Grades,
    SingleGrade,
    GradesByCourseCode,
    AllGradesByAdminNum,
)
from .courses.views import Course, SingleCourse

BLUEPRINT = Blueprint("api", __name__, url_prefix="/api")
API = Api(BLUEPRINT)

API.add_resource(UserSignUp, "/auth/signup")
API.add_resource(UserSignIn, "/auth/signin")
API.add_resource(Users, "/users")
API.add_resource(Search, "/users/<string:admission_number>")
API.add_resource(UserAdminStatus, "/users/<string:admission_number>/status")
API.add_resource(Grades, "/grades")
API.add_resource(
    SingleGrade,
    "/grades/courses/<string:course_code>/students/<string:admission_number>",
)
API.add_resource(GradesByCourseCode, "/grades/courses/<string:course_code>")
API.add_resource(AllGradesByAdminNum, "/grades/students/<string:admission_number>")
API.add_resource(Course, "/course")
API.add_resource(SingleCourse, "/courses/<string:course_code>")
