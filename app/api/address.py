from typing import Any, Optional
from fastapi import APIRouter, HTTPException

from app.dto.pagination import PaginationDTO
from app.services.address import get_address


router = APIRouter()

@router.get("/", response_model=PaginationDTO[Any])
async def get_address_api(
    country: Optional[str] = None,
    city: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    try:
        return await get_address(city, country, page, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))