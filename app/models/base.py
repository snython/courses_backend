from mongoengine import Document, DateTimeField
from bson import DBRef, ObjectId
from datetime import datetime, timezone

class BaseModel(Document):
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'abstract': True  # Indicates this is a base class and won't be a collection itself
    }

    def to_dict(self):
        data = self.to_mongo().to_dict()

        def convert_object_id(value):
            if isinstance(value, ObjectId):
                return str(value)
            elif isinstance(value, datetime):
                return value.isoformat()
            elif isinstance(value, Document):
                # Convert MongoEngine documents to dict
                return value.to_dict()
            elif hasattr(value, 'to_dict') and callable(value.to_dict):
                # Convert custom class instances to dict using their to_dict method
                return value.to_dict()
            elif isinstance(value, dict):
                return {k: convert_object_id(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [convert_object_id(v) for v in value]
            else:
                return value
        data = convert_object_id(data)

        # Replace the _id field with id
        if '_id' in data:
            data['id'] = data.pop('_id')

        return data
