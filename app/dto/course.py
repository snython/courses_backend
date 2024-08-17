from pydantic import BaseModel
from typing import Optional

class CreateCourseDTO(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: str
    end_date: str
    price: float
    currency: str
    university_id: str
    country: str
    city: str


class UpdateCourseDTO(BaseModel):
    currency: str
    price: float
    start_date: str
    end_date: str
    description: Optional[str] = None