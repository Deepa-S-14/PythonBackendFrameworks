from pydantic import BaseModel


class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int


class CourseResponse(CourseCreate):
    id: int