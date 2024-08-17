from mongoengine import StringField, DateField, FloatField, ReferenceField
from app.models.base import BaseModel
from app.models.university import University


class Address(BaseModel):
    city = StringField(required=True)
    country = StringField(required=True)

    meta = {
        'indexes': [
            {
                'fields': ('city', 'country'),
                'unique': True
            },
            {
                'fields': ['city'],
                'name': 'city_index'  # Named index for city
            },
            {
                'fields': ['country'],
                'name': 'country_index'  # Named index for country
            },
            {
                'fields': ['city', 'country'],
                'name': 'city_country_index'  # Named composite index for city and country
            }
        ]
    }

class Course(BaseModel):
    name = StringField(required=True)
    description = StringField()
    start_date = DateField()
    end_date = DateField()
    price = FloatField()
    currency = StringField()
    location:Address = ReferenceField(Address, required=True)
    university:University = ReferenceField(University, required=True)

    meta = {
        'indexes': [
            {
                'fields': ('name', 'university', 'location'),
                'unique': True
            }
        ]
    }