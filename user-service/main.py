import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.web.routers import users
from app.data.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="User Service",
    description="User management for ride-sharing system",
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

# Include routers
app.include_router(users.router, prefix="/api/v1", tags=["users"])

# Health check endpoint
@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy", "service": "user-service"}

# Main entry point
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("SERVICE_PORT", "8001"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)