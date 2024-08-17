from typing import Dict, Any
from math import ceil
from mongoengine.queryset import QuerySet

from app.dto.pagination import PaginationDTO

def get_paginated_results(
    query: QuerySet,
    page: int,
    page_size: int,
) -> PaginationDTO:
    """
    Utility function to handle pagination for a given query.

    :param query: The MongoEngine query object to paginate.
    :param page: The current page number (1-based index).
    :param page_size: The number of items per page.
    :param model_type: The model type of the query results.
    :return: A dictionary with pagination information and results.
    """
    # Calculate pagination parameters
    total_items = query.count()
    total_pages = ceil(total_items / page_size)
    skip = (page - 1) * page_size
    
    # Apply pagination to the query
    results = query.skip(skip).limit(page_size).select_related()
    
    # Convert results to list of model_type instances
    items = [r.to_dict() for r in list(results)]
    
    # Create the pagination information
    pagination_info: PaginationDTO = {
        'total_items': total_items,
        'total_pages': total_pages,
        'current_page': page,
        'page_size': page_size,
        'has_next': page < total_pages,
        'has_previous': page > 1,
        'items': items
    }
    
    return pagination_info

