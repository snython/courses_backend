from mongoengine import StringField

from app.config.settings import settings
from app.models.base import BaseModel


class University(BaseModel):
    name = StringField(required=True)

    meta = {
        'indexes': [
            {
                'fields': ['created_at'],
                'expireAfterSeconds': settings.mongo_ttl_seconds,
            }
        ]
    }