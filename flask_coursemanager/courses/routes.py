from flask import Blueprint, jsonify, request
from courses.models import Course, db

courses_bp = Blueprint(
    "courses",
    __name__,
    url_prefix="/api/courses"
)


def make_response_json(data, status_code=200):
    return jsonify({
        "status": "success",
        "data": data
    }), status_code


@courses_bp.route("/", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    data = [course.to_dict() for course in courses]
    return make_response_json(data)


@courses_bp.route("/<int:course_id>", methods=["GET"])
def get_course(course_id):
    course = Course.query.get(course_id)

    if not course:
        return jsonify({
            "error": "Course not found"
        }), 404

    return make_response_json(course.to_dict())


@courses_bp.route("/", methods=["POST"])
def create_course():
    data = request.get_json()

    if data is None:
        return jsonify({
            "error": "Request body must be JSON"
        }), 400

    required_fields = ["name", "code", "credits", "department_id"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    course = Course(
        name=data["name"],
        code=data["code"],
        credits=data["credits"],
        department_id=data["department_id"]
    )

    db.session.add(course)
    db.session.commit()

    return make_response_json(course.to_dict(), 201)


@courses_bp.route("/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    course = Course.query.get(course_id)

    if not course:
        return jsonify({
            "error": "Course not found"
        }), 404

    data = request.get_json()

    if data is None:
        return jsonify({
            "error": "Request body must be JSON"
        }), 400

    course.name = data.get("name", course.name)
    course.code = data.get("code", course.code)
    course.credits = data.get("credits", course.credits)
    course.department_id = data.get("department_id", course.department_id)

    db.session.commit()

    return make_response_json(course.to_dict())


@courses_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    course = Course.query.get(course_id)

    if not course:
        return jsonify({
            "error": "Course not found"
        }), 404

    db.session.delete(course)
    db.session.commit()

    return make_response_json({
        "message": "Course deleted"
    })