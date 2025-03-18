from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.web.routers import riders
from app.data.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rider Service",
    description="Rider management for ride-sharing system",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include rider router
app.include_router(riders.router, prefix="/api/v1", tags=["riders"])
