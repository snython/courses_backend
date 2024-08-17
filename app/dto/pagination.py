from typing import List, TypeVar, Generic, Dict, Any
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class PaginationDTO(BaseModel, Generic[T]):
    total_items: int
    total_pages: int
    current_page: int
    page_size: int
    has_next: bool
    has_previous: bool
    items: List[T]

    def __init__(self, **data):
        super().__init__(**data)