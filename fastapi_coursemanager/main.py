from fastapi import FastAPI, Depends, HTTPException, Response, status
from schemas import CourseCreate, CourseUpdate
from database import get_db

app = FastAPI(
    title="Course Manager API",
    description="RESTful API following best practices",
    version="2.0.0",
)

courses = []
next_id = 1


def error_response(code: str, message: str, field=None):
    return {
        "error": {
            "code": code,
            "message": message,
            "field": field
        }
    }


@app.get("/", tags=["Home"])
async def root():
    return {"message": "Welcome to Course Manager API v1"}


# URL Versioning: /api/v1/
# Another common approach is header-based versioning
# (Accept: application/vnd.api+json;version=1)


@app.get("/api/v1/courses", tags=["Courses"])
async def get_courses(
    page: int = 1,
    page_size: int = 10,
    search: str = "",
    db=Depends(get_db)
):
    filtered = courses

    if search:
        filtered = [
            c for c in courses
            if search.lower() in c["name"].lower()
            or search.lower() in c["code"].lower()
        ]

    total = len(filtered)

    start = (page - 1) * page_size
    end = start + page_size

    results = filtered[start:end]

    next_page = (
        f"/api/v1/courses?page={page+1}&page_size={page_size}"
        if end < total else None
    )

    previous_page = (
        f"/api/v1/courses?page={page-1}&page_size={page_size}"
        if page > 1 else None
    )

    return {
        "count": total,
        "next": next_page,
        "previous": previous_page,
        "results": results
    }


@app.get("/api/v1/courses/{course_id}", tags=["Courses"])
async def get_course(course_id: int):

    for course in courses:
        if course["id"] == course_id:
            return course

    raise HTTPException(
        status_code=404,
        detail=error_response(
            "NOT_FOUND",
            f"Course with id {course_id} does not exist"
        )
    )


@app.post(
    "/api/v1/courses",
    tags=["Courses"],
    status_code=status.HTTP_201_CREATED,
    summary="Create Course",
    response_description="Created Course"
)
async def create_course(
    course: CourseCreate,
    response: Response,
    db=Depends(get_db)
):
    global next_id

    new_course = {
        "id": next_id,
        "name": course.name,
        "code": course.code,
        "credits": course.credits
    }

    courses.append(new_course)

    response.headers["Location"] = f"/api/v1/courses/{next_id}"

    next_id += 1

    return new_course


@app.put("/api/v1/courses/{course_id}", tags=["Courses"])
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
            return course

    raise HTTPException(
        status_code=404,
        detail=error_response(
            "NOT_FOUND",
            f"Course with id {course_id} does not exist"
        )
    )


@app.patch("/api/v1/courses/{course_id}", tags=["Courses"])
async def patch_course(
    course_id: int,
    updated: CourseUpdate,
    db=Depends(get_db)
):
    for course in courses:
        if course["id"] == course_id:

            if updated.name is not None:
                course["name"] = updated.name

            if updated.code is not None:
                course["code"] = updated.code

            if updated.credits is not None:
                course["credits"] = updated.credits

            return course

    raise HTTPException(
        status_code=404,
        detail=error_response(
            "NOT_FOUND",
            f"Course with id {course_id} does not exist"
        )
    )


@app.delete(
    "/api/v1/courses/{course_id}",
    tags=["Courses"],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_course(
    course_id: int,
    db=Depends(get_db)
):
    for course in courses:
        if course["id"] == course_id:
            courses.remove(course)
            return

    raise HTTPException(
        status_code=404,
        detail=error_response(
            "NOT_FOUND",
            f"Course with id {course_id} does not exist"
        )
    )