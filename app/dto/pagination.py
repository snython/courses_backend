from typing import List, TypeVar, Generic, Dict, Any
from math import ceil
from mongoengine.queryset import QuerySet

from app.models.base import BaseModel

T = TypeVar('T')

class PaginationDTO(BaseModel, Generic[T]):
    total_items: int
    total_pages: int
    current_page: int
    page_size: int
    has_next: bool
    has_previous: bool
    items: List[T]