import pandas as pd
import requests
import io
from datetime import datetime
from app.models.university import University
from app.models.course import Course, Address
from app.config.settings import settings
from app.config.logger import logger

async def load_and_normalize_data():
    # Check if any university data exists
    if University.objects.count() > 0:
        # If data exists and is not expired, no need to reload
        logger.info("Data already exists and is not expired.")
        return

    # Otherwise, reload the data
    logger.info("Data is expired or missing. Reloading...")

    response = requests.get(settings.csv_url)
    csv_data = response.content.decode('utf-8')

    # Use io.StringIO to handle the CSV data in memory
    df = pd.read_csv(io.StringIO(csv_data))

    for _, row in df.iterrows():
        university = University.objects(name=row["University"]).first()

        if not university:
            university = University(name=row["University"], created_at=datetime.utcnow())
            university.save()

        location = Address.objects(city=row["City"], country=row["Country"]).first()

        if not location:
            location = Address(city=row["City"], country=row["Country"])
            location.save()

        course = Course(
            name=row["CourseName"],
            description=row["CourseDescription"],
            start_date=pd.to_datetime(row["StartDate"]).date(),
            end_date=pd.to_datetime(row["EndDate"]).date(),
            price=row["Price"],
            currency=row["Currency"],
            university=university,
            location=location
        )
        course.save()
