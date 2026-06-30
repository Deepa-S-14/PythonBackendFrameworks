from fastapi import FastAPI, Depends
from schemas import CourseCreate
from database import get_db

app = FastAPI(
    title="Course Manager API",
    description="FastAPI CRUD API with Dependency Injection",
    version="1.0.0"
)

courses = []
next_id = 1


@app.get("/", tags=["Home"], summary="Welcome Endpoint")
async def root():
    return {"message": "Welcome to Course Manager API"}


@app.get(
    "/courses",
    tags=["Courses"],
    summary="Get all courses",
    description="Returns a list of all available courses."
)
async def get_courses(db=Depends(get_db)):
    return {
        "message": "All courses",
        "data": courses
    }


@app.get(
    "/courses/{course_id}",
    tags=["Courses"],
    summary="Get course by ID"
)
async def get_course(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            return course
    return {"error": "Course not found"}


@app.post(
    "/courses",
    tags=["Courses"],
    summary="Create a new course"
)
async def create_course(course: CourseCreate, db=Depends(get_db)):
    global next_id

    new_course = {
        "id": next_id,
        "name": course.name,
        "code": course.code,
        "credits": course.credits
    }

    courses.append(new_course)
    next_id += 1

    return {
        "message": "Course created successfully",
        "course": new_course
    }


@app.put(
    "/courses/{course_id}",
    tags=["Courses"],
    summary="Update an existing course"
)
async def update_course(
    course_id: int,
    updated_course: CourseCreate,
    db=Depends(get_db)
):
    for course in courses:
        if course["id"] == course_id:
            course["name"] = updated_course.name
            course["code"] = updated_course.code
            course["credits"] = updated_course.credits

            return {
                "message": "Course updated successfully",
                "course": course
            }

    return {"error": "Course not found"}


@app.delete(
    "/courses/{course_id}",
    tags=["Courses"],
    summary="Delete a course"
)
async def delete_course(course_id: int, db=Depends(get_db)):
    for course in courses:
        if course["id"] == course_id:
            courses.remove(course)
            return {"message": "Course deleted successfully"}

    return {"error": "Course not found"}