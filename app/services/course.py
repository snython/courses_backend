import math
from typing import Any, Dict, Optional
from mongoengine import Q
from mongoengine.errors import DoesNotExist, ValidationError
from app.models.course import Course
from app.models.university import University
from app.models.course import Address
from app.dto.course import CreateCourseDTO, UpdateCourseDTO
from app.config.logger import logger
from app.dto.pagination import PaginationDTO
from app.utils.util import map_course_to_dict

async def get_courses(
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 10
):

    pipeline = [
        {
            '$lookup': {
                'from': 'university',  # Collection name for University
                'localField': 'university',  # Field in Course
                'foreignField': '_id',  # Field in University
                'as': 'university'
            }
        },
        {
            '$unwind': '$university'
        },
        {
            '$lookup': {
                'from': 'address',  # Collection name for University
                'localField': 'location',  # Field in Course
                'foreignField': '_id',  # Field in University
                'as': 'location'
            }
        },
        {
            '$unwind': '$location'
        },
        {
            '$addFields': {
                'id': { '$toString': "$_id" },
            }
        },
    ]

    if search:
        pipeline.append({
            '$match': {
                '$or': [
                    {'name': {'$regex': search, '$options': 'i'}},
                    {'university.name': {'$regex': search, '$options': 'i'}},
                    {'location.city': {'$regex': search, '$options': 'i'}},
                    {'location.country': {'$regex': search, '$options': 'i'}}
                ]
            }
        })
    
    count_pipeline = pipeline.copy()
    count_pipeline.extend([{ "$count": "count" }])
    result_count = list(Course.objects.aggregate(count_pipeline))

    total_items = result_count[0]["count"] if len(result_count) > 0 else 0
    skip = (page - 1) * page_size
    results = []
    
    if total_items > 0:
                pipeline.extend([
                {
                    '$addFields': {
                        'id': { '$toString': "$_id" },
                        'location.id': '$location._id',
                        'university.id': '$university._id'
                    }
                },
                {
                    '$project': { 
                         "_id": 0,
                         'location._id': 0,
                         'university._id': 0
                    }
                },
                    { "$skip": skip },
                    { "$limit": page_size }
                ])
                results = list(Course.objects.aggregate(pipeline))

    total_pages = math.ceil(total_items / page_size)

    return PaginationDTO[Dict[str, Any]](
        total_items = total_items,
        total_pages =  total_pages,
        current_page = page,
        page_size = page_size,
        has_next = page < total_pages,
        has_previous = page > 1,
        items = [ Course(**r).to_dict() for r in results ]
    )


async def create_course(course_data: CreateCourseDTO) -> Dict[str, Any]:
    try:
        #TODO: validation check that start date < end date
        #TODO: check if course already exists return validation error
        university = University.objects.get(id=course_data.university_id)
        location = Address.objects(city=course_data.city, country=course_data.country).first()
        if not location:
            location = Address(city=course_data.city, country=course_data.country)
            location.save()

        course = Course(
            name=course_data.name,
            description=course_data.description,
            start_date=course_data.start_date,
            end_date=course_data.end_date,
            price=course_data.price,
            currency=course_data.currency,
            university=university,
            location=location
        )
        course.save()
        return map_course_to_dict(course)
    except (DoesNotExist, ValidationError) as e:
        logger.error(f"Failed to create course: {e}")
        raise e

async def update_course(course_id: str, course_data: UpdateCourseDTO) -> Dict[str, Any]:
    try:
        course = Course.objects.get(id=course_id)
        
        course.currency = course_data.currency
        course.price = course_data.price
        course.start_date = course_data.start_date
        course.end_date = course_data.end_date
        course.description = course_data.description

        course = course.save()
        return map_course_to_dict(course)
    except (DoesNotExist, ValidationError) as e:
        logger.error(f"Failed to update course: {e}")
        raise e

async def delete_course(course_id: str) -> Dict[str, Any]:
    try:
        course = Course.objects.get(id=course_id)
        course.delete()
        return map_course_to_dict(course)
    except DoesNotExist as e:
        logger.error(f"Failed to delete course: {e}")
        raise e
