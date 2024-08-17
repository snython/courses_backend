from pydantic import BaseModel
from typing import Optional

class CourseDTO(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    university: str