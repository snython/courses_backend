from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.mongo import init_db
from app.services.data_loader import load_and_normalize_data
from app.api import course, currency, university, address
from app.config.settings import settings

app = FastAPI()

# Define the startup event handler
async def on_startup():
    init_db()
    await load_and_normalize_data()

# Add the startup event handler
app.add_event_handler("startup", on_startup)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include API routers
app.include_router(course.router, prefix="/courses")
app.include_router(university.router, prefix="/universities")
app.include_router(address.router, prefix="/addresses")
app.include_router(currency.router, prefix="/currencies")

@app.get("/")
async def root():
    return {"message": "University Data Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.app_host, port=settings.app_port, reload=settings.app_reload)
