from typing import Any, Optional
from fastapi import APIRouter, HTTPException

from app.dto.pagination import PaginationDTO
from app.services.university import get_universities

router = APIRouter()

@router.get("/", response_model=PaginationDTO[Any])
async def get_universities_api(
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    try:
        return await get_universities(search, page, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))