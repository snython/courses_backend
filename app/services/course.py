import math
from typing import Any, List, Optional
from mongoengine import Q
from mongoengine.errors import DoesNotExist, ValidationError
from app.models.course import Course
from app.models.university import University
from app.dto.course import CourseDTO
from app.config.logger import logger
from app.dto.pagination import PaginationDTO

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

    courses: list[Course] = []
    total_items = result_count[0]["count"] if len(result_count) > 0 else 0
    skip = (page - 1) * page_size

    if total_items > 0:
                pipeline.extend([
                {
                    '$addFields': {
                        'id': { '$toString': "$_id" },
                    }
                },
                {
                    '$project': { "_id": 0 }
                },
                    { "$skip": skip },
                    { "$limit": page_size }
                ])
                results = list(Course.objects.aggregate(pipeline))
                for c in results:
                    data = Course(**c).to_dict()
                    data['university']['id'] = data['university']['_id']
                    data['location']['id'] = data['location']['_id']
                    del data['university']['_id']
                    del data['location']['_id']
                    courses.append(data)

    total_pages = math.ceil(total_items / page_size)

    return {
         "total_items":total_items,
        "total_pages": total_pages,
        "current_page": page,
        "page_size": page_size,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "items": courses
    }


async def create_course(course_data: CourseDTO) -> str:
    try:
        university = University.objects.get(id=course_data.university)
        course = Course(
            name=course_data.name,
            description=course_data.description,
            start_date=course_data.start_date,
            end_date=course_data.end_date,
            price=course_data.price,
            currency=course_data.currency,
            university=university
        )
        course.save()
        return str(course.id)
    except (DoesNotExist, ValidationError) as e:
        logger.error(f"Failed to create course: {e}")
        raise e

async def update_course(course_id: str, course_data: CourseDTO) -> str:
    try:
        course = Course.objects.get(id=course_id)
        course.update(**course_data.dict(exclude_unset=True))
        return "Course updated successfully"
    except (DoesNotExist, ValidationError) as e:
        logger.error(f"Failed to update course: {e}")
        raise e

async def delete_course(course_id: str) -> str:
    try:
        course = Course.objects.get(id=course_id)
        course.delete()
        return "Course deleted successfully"
    except DoesNotExist as e:
        logger.error(f"Failed to delete course: {e}")
        raise e
