import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import matching
from app.distance_matrix import DistanceMatrixService

# Initialize FastAPI app
app = FastAPI(
    title="Ride Matching Service",
    description="Service for matching users with the nearest available riders",
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

# Dependency injection
def get_distance_service():
    return DistanceMatrixService()

# Override the dependency in the router
app.dependency_overrides[DistanceMatrixService] = get_distance_service

# Include routers
app.include_router(matching.router, prefix="/api/v1", tags=["matching"])

# Health check endpoint
@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy", "service": "ride-matching-service"}

# Main entry point
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("SERVICE_PORT", "8004"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)