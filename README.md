# StudentsRegistry

### What it does

The Students Registry is a simple registry that records students' details and grades.

### Tech/framework used

- python 3.8.10
- [Flask](https://flask.palletsprojects.com/en/latest/)

## Installation and Deployment.

### Getting Started

```bash
git clone https://github.com/ogambakerubo/StudentsRegistry.git
cd StudentsRegistry
touch .env
```

### Seting up databases

Create two Postgres databases and change the values of the database URLs in the `.env` file

```bash
sudo -u postgres psql
postgres=# create database studentsregistry;
postgres=# create database teststudentsregistry;
```

### Create a virtual environment and activate it

```bash
python3 -m venv env
source venv/bin/activate
```

### Install all the dependencies using the command

```bash
pip install -r requirements.txt
```

### Contents of .env file

```
export FLASK_APP="run.py"
export FLASK_ENV="development"
export FLASK_CONFIG="development"
export DATABASE_URL="dbname='your-database' host='localhost' port='5432' user='your-username' password='your-password'"
export DATABASE_URL_TEST="dbname='your-test-database' host='localhost' port='5432' user='your-username' password='your-password'"
export SECRET_KEY="secret-key-goes-here"
```

### How to Run the App

```bash
source venv/bin/activate
flask run
```

### Test the application

Tests are run with pytest or py.test in the root folder.
Set FLASK_CONFIG to testing on your .env file before running tests

```bash
source venv/bin/activate
pytest --cov=app/
```

### Endpoints to test

| Method | Endpoint                                                                      | Description                             |
| ------ | ----------------------------------------------------------------------------- | --------------------------------------- |
| POST   | `/api/auth/signup/`                                                           | Sign up a new user.                     |
| POST   | `/api/auth/signin/`                                                           | Sign in an existing user/administrator. |
| GET    | `/api/users`                                                                  | Fetch all users.                        |
| GET    | `/api/users/<string:admission_number>`                                        | Fetch user by admission number.         |
| GET    | `/api/users/<string:admission_number>`                                        | Delete user by admission number.        |
| PATCH  | `/api/users/<string:admission_number>/status`                                 | Set existing user to admin.             |
| POST   | `/api/course`                                                                 | Create a new course.                    |
| GET    | `/api/courses/<string:course_code>`                                           | Fetch a course by course code.          |
| PATCH  | `/api/courses/<string:course_code>`                                           | Update course details.                  |
| DELETE | `/api/courses/<string:course_code>`                                           | Delete a course.                        |
| POST   | `/api/grades`                                                                 | Create a new grade entry.               |
| GET    | `/api/grades/courses/<string:course_code>/students/<string:admission_number>` | Get a grade entry by a student.         |
| PATCH  | `/api/grades/courses/<string:course_code>/students/<string:admission_number>` | Update grade entry by a student.        |
| DELETE | `/api/grades/courses/<string:course_code>/students/<string:admission_number>` | Delete grade entry by a student.        |
| GET    | `/api/grades/courses/<string:course_code>`                                    | Fetch grade entries by course code.     |
| PATCH  | `/api/grades/students/<string:admission_number>`                              | Fetch grade entries by a student.       |

### Documentation

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/9aa12f22e17048d529dc)
