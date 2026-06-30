from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Course(BaseModel):
    name: str
    code: str
    credits: int


@app.get("/")
async def root():
    return {"message": "Welcome to Course Manager API"}


@app.get("/courses/{course_id}")
async def get_course(course_id: int):
    return {
        "course_id": course_id,
        "message": f"Course {course_id} found"
    }


@app.get("/search")
async def search_courses(name: str = None):
    if name:
        return {
            "message": f"Searching for '{name}'"
        }

    return {
        "message": "Returning all courses"
    }


@app.post("/courses")
async def create_course(course: Course):
    return {
        "message": "Course created successfully",
        "course": course
    }