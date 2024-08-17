from fastapi import APIRouter, HTTPException
from typing import Any, Dict, Optional
from app.dto.course import CreateCourseDTO, UpdateCourseDTO
from app.dto.pagination import PaginationDTO
from app.services.course import get_courses, create_course, update_course, delete_course

router = APIRouter()

@router.get("/", response_model=PaginationDTO[Any])
async def get_courses_api(
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    try:
        return await get_courses(search, page, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=Dict[str, Any])
async def create_course_api(course_data: CreateCourseDTO):
    try:
        course_id = await create_course(course_data)
        return course_id
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{course_id}", response_model=Dict[str, Any])
async def update_course_api(course_id: str, course_data: UpdateCourseDTO):
    try:
        result = await update_course(course_id, course_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{course_id}", response_model=str)
async def delete_course_api(course_id: str):
    try:
        result = await delete_course(course_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="Course not found")
