from app.models.course import Course


def get_currencies() -> list[str]:
    pipeline = [
        {"$group": {"_id": None, "currencies": {"$addToSet": "$currency"}}},
        {"$project": {"_id": 0, "currencies": 1}}
    ]

    query_result = Course.objects.aggregate(pipeline)
    data = [r for r in query_result]
    return data[0]["currencies"] if data else []