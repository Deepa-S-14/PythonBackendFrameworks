from typing import Optional
from pydantic import BaseModel


class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None


class CourseResponse(CourseCreate):
    id: int