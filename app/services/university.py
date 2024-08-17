import math
from typing import Any, Dict, Optional
from mongoengine import Q

from app.dto.pagination import PaginationDTO
from app.models.university import University

async def get_universities(
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 10
) -> PaginationDTO[Dict[str, Any]]:
    query = Q()
    if search:
        query |= Q(name__icontains=search)
    
    skip = (page - 1) * page_size
    results = University.objects(query).skip(skip).limit(page_size)
    total_items = University.objects(query).count()
    total_pages = math.ceil(total_items / page_size)

    return PaginationDTO[Dict[str, Any]](
        total_items = total_items,
        total_pages =  total_pages,
        current_page = page,
        page_size = page_size,
        has_next = page < total_pages,
        has_previous = page > 1,
        items = [r.to_dict() for r in results]
    )