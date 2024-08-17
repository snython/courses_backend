from typing import Dict, Any

from app.models.course import Course

def map_course_to_dict(course: Course) -> Dict[str, Any]:
    location = course.location
    university = course.university
    course_dict = course.to_dict()
    course_dict['university'] = university.to_dict()
    course_dict['location'] = location.to_dict()
    return course_dict

