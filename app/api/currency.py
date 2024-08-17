from fastapi import APIRouter, HTTPException

from app.services.currency import get_currencies

router = APIRouter()

@router.get("/", response_model=list[str])
async def get_currencies_api():
    try:
        return get_currencies()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))