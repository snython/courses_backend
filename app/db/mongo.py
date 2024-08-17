from mongoengine import connect
from app.config.settings import settings

def init_db():
    connect(db=settings.mongo_db, host=settings.mongo_host, port=settings.mongo_port)