from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
import random

from app.database import get_db
from app.models import Rider, DistanceMatrix
from app.schemas import (
    RiderCreate, RiderResponse, RiderUpdate,
    DistanceMatrixCreate, DistanceMatrixResponse,
    NearestRiderRequest, NearestRiderResponse
)

router = APIRouter()

@router.post("/riders", response_model=RiderResponse, status_code=status.HTTP_201_CREATED)
def create_rider(rider: RiderCreate, db: Session = Depends(get_db)):
    # Check if rider with user_id already exists
    db_rider = db.query(Rider).filter(Rider.user_id == rider.user_id).first()
    if db_rider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rider with this user_id already exists"
        )
    
    # Check if license plate is already registered
    existing_license = db.query(Rider).filter(Rider.license_plate == rider.license_plate).first()
    if existing_license:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle with this license plate is already registered"
        )
    
    # Create new rider
    db_rider = Rider(**rider.dict())
    db.add(db_rider)
    db.commit()
    db.refresh(db_rider)
    return db_rider

@router.get("/riders", response_model=List[RiderResponse])
def read_riders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    riders = db.query(Rider).offset(skip).limit(limit).all()
    return riders

@router.get("/riders/{rider_id}", response_model=RiderResponse)
def read_rider(rider_id: int, db: Session = Depends(get_db)):
    rider = db.query(Rider).filter(Rider.id == rider_id).first()
    if rider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rider not found")
    return rider

@router.patch("/riders/{rider_id}", response_model=RiderResponse)
def update_rider(rider_id: int, rider_update: RiderUpdate, db: Session = Depends(get_db)):
    db_rider = db.query(Rider).filter(Rider.id == rider_id).first()
    if db_rider is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rider not found")
    
    # Update rider fields if provided
    update_data = rider_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_rider, key, value)
    
    db.commit()
    db.refresh(db_rider)
    return db_rider

@router.post("/distance-matrix", response_model=DistanceMatrixResponse)
def create_distance_entry(entry: DistanceMatrixCreate, db: Session = Depends(get_db)):
    # Check if entry already exists
    existing_entry = db.query(DistanceMatrix).filter(
        DistanceMatrix.user_id == entry.user_id,
        DistanceMatrix.rider_id == entry.rider_id
    ).first()
    
    if existing_entry:
        # Update existing entry
        existing_entry.distance_km = entry.distance_km
        db.commit()
        db.refresh(existing_entry)
        return existing_entry
    
    # Create new entry
    db_entry = DistanceMatrix(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.get("/nearest-rider", response_model=NearestRiderResponse)
def find_nearest_rider(request: NearestRiderRequest, db: Session = Depends(get_db)):
    # Find all available riders
    available_riders = db.query(Rider).filter(Rider.status == "Available").all()
    if not available_riders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No available riders found"
        )
    
    # Get rider IDs
    available_rider_ids = [rider.id for rider in available_riders]
    
    # Find distances for available riders
    distances = db.query(DistanceMatrix).filter(
        DistanceMatrix.user_id == request.user_id,
        DistanceMatrix.rider_id.in_(available_rider_ids)
    ).all()
    
    if not distances:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No distance information found for this user and available riders"
        )
    
    # Find the minimum distance
    min_distance = min(distances, key=lambda x: x.distance_km)
    
    # Find all riders with the minimum distance (in case there are multiple)
    closest_riders = [d for d in distances if d.distance_km == min_distance.distance_km]
    
    # If there are multiple riders with the same minimum distance, choose one randomly
    if len(closest_riders) > 1:
        chosen_rider = random.choice(closest_riders)
    else:
        chosen_rider = closest_riders[0]
    
    return {
        "rider_id": chosen_rider.rider_id,
        "distance_km": float(chosen_rider.distance_km)
    }