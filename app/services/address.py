import math
from typing import Any, Dict, Optional
from app.dto.pagination import PaginationDTO
from mongoengine import Q

from app.models.course import Address

async def get_address(
    city: Optional[str] = None,
    country: Optional[str] = None,
    page: int = 1,
    page_size: int = 10
) -> PaginationDTO[Dict[str, Any]]:
    query = Q()
    if city:
        query &= Q(city__icontains=city)
    
    if country:
        query &= Q(country__icontains=country)

    if not city:  # Return only distinct countries if city is not provided
        distinct_countries = Address.objects(query).distinct('country')
        total_items = len(distinct_countries)
        total_pages = math.ceil(total_items / page_size)
        skip = (page - 1) * page_size

        # Paginate the list of distinct countries
        paginated_countries = distinct_countries[skip:skip + page_size]
        
        return PaginationDTO[Dict[str, Any]](
            total_items=total_items,
            total_pages=total_pages,
            current_page=page,
            page_size=page_size,
            has_next=page < total_pages,
            has_previous=page > 1,
            items=[{'country': country} for country in paginated_countries]
        )
    
    skip = (page - 1) * page_size
    results = Address.objects(query).skip(skip).limit(page_size)
    total_items = Address.objects(query).count()
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