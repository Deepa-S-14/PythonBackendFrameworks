from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Response,
    status
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from schemas import CourseCreate, CourseUpdate
from database import get_db
from auth import (
    hash_password,
    verify_password,
    create_access_token
)

app = FastAPI(
    title="Course Manager API",
    description="RESTful API with Authentication",
    version="3.0.0"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

courses = []
next_id = 1

# Demo user
users = {
    "admin": {
        "username": "admin",
        "hashed_password": hash_password("admin123")
    }
}


def error_response(code: str, message: str, field=None):
    return {
        "error": {
            "code": code,
            "message": message,
            "field": field
        }
    }


@app.get("/")
async def root():
    return {"message": "Welcome to Secure Course Manager API"}


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = users.get(form_data.username)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        user["hashed_password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": user["username"]}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    return {
        "message": "Access Granted",
        "token": token
    }


@app.get("/api/v1/courses")
async def get_courses(db=Depends(get_db)):
    return courses


@app.post("/api/v1/courses")
async def create_course(
    course: CourseCreate,
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
    next_id += 1

    return new_course


@app.put("/api/v1/courses/{course_id}")
async def update_course(
    course_id: int,
    updated: CourseCreate,
    db=Depends(get_db)
):
    for course in courses:
        if course["id"] == course_id:
            course["name"] = updated.name
            course["code"] = updated.code
            course["credits"] = updated.credits
            return course

    raise HTTPException(status_code=404, detail="Course not found")


@app.patch("/api/v1/courses/{course_id}")
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

    raise HTTPException(status_code=404, detail="Course not found")


@app.delete("/api/v1/courses/{course_id}")
async def delete_course(
    course_id: int,
    db=Depends(get_db)
):
    for course in courses:
        if course["id"] == course_id:
            courses.remove(course)
            return {
                "message": "Course deleted successfully"
            }

    raise HTTPException(status_code=404, detail="Course not found")