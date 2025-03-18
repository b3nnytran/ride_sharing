from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.data.database import get_db
from app.data.schemas import RiderCreate, RiderResponse, RiderUpdate, DistanceMatrixCreate, DistanceMatrixResponse
from app.service.rider_service import (
    create_rider_service, get_rider_service, get_all_riders_service,
    update_rider_service, create_distance_entry_service
)

router = APIRouter()

@router.post("/riders", response_model=RiderResponse)
def create_rider(rider: RiderCreate, db: Session = Depends(get_db)):
    """Register a new rider."""
    new_rider = create_rider_service(rider, db)
    if not new_rider:
        raise HTTPException(status_code=400, detail="Rider already exists")
    return new_rider

@router.get("/riders", response_model=List[RiderResponse])
def get_riders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all riders."""
    return get_all_riders_service(db, skip, limit)

@router.get("/riders/{rider_id}", response_model=RiderResponse)
def get_rider(rider_id: int, db: Session = Depends(get_db)):
    """Get a specific rider."""
    rider = get_rider_service(rider_id, db)
    if not rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    return rider

@router.patch("/riders/{rider_id}", response_model=RiderResponse)
def update_rider(rider_id: int, rider_update: RiderUpdate, db: Session = Depends(get_db)):
    """Update a rider's details."""
    updated_rider = update_rider_service(rider_id, rider_update, db)
    if not updated_rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    return updated_rider
