import os
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import random

from app.database import get_db
from app.models import Ride
from app.schemas import RideCreate, RideResponse, RideUpdate, RideRequest, RiderMatchResponse
from app.fare import calculate_fare

router = APIRouter()

# Get URL for the ride matching service from environment variables
RIDE_MATCHING_SERVICE_URL = os.getenv("RIDE_MATCHING_SERVICE_URL", "http://ride-matching-service:8004")

@router.post("/rides/request", response_model=RideResponse)
async def request_ride(ride_request: RideRequest, db: Session = Depends(get_db)):
    """Request a new ride by finding the nearest available rider"""
    
    # Call the ride matching service to find the nearest rider
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{RIDE_MATCHING_SERVICE_URL}/api/v1/match",
                json={"user_id": ride_request.user_id}
            )
            response.raise_for_status()
            match_result = response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Error finding nearest rider: {str(e)}"
            )
    
    # Extract rider_id and distance from match result
    rider_id = match_result["rider_id"]
    distance_km = match_result["distance_km"]
    
    # Calculate fare based on distance
    fare_amount = calculate_fare(distance_km)
    
    # Create a new ride in the database
    new_ride = Ride(
        user_id=ride_request.user_id,
        rider_id=rider_id,
        pickup_location=ride_request.pickup_location,
        dropoff_location=ride_request.dropoff_location,
        distance_km=distance_km,
        fare_amount=fare_amount,
        status="Pending"
    )
    
    db.add(new_ride)
    db.commit()
    db.refresh(new_ride)
    
    return new_ride

@router.get("/rides", response_model=List[RideResponse])
def get_rides(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get a list of all rides"""
    rides = db.query(Ride).offset(skip).limit(limit).all()
    return rides

@router.get("/rides/{ride_id}", response_model=RideResponse)
def get_ride(ride_id: int, db: Session = Depends(get_db)):
    """Get details of a specific ride"""
    ride = db.query(Ride).filter(Ride.id == ride_id).first()
    if ride is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ride not found")
    return ride

@router.patch("/rides/{ride_id}/status", response_model=RideResponse)
def update_ride_status(ride_id: int, ride_update: RideUpdate, db: Session = Depends(get_db)):
    """Update the status of a ride"""
    ride = db.query(Ride).filter(Ride.id == ride_id).first()
    if ride is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ride not found")
    
    # Update ride status
    ride.status = ride_update.status
    db.commit()
    db.refresh(ride)
    
    return ride

@router.get("/users/{user_id}/rides", response_model=List[RideResponse])
def get_user_rides(user_id: int, db: Session = Depends(get_db)):
    """Get all rides for a specific user"""
    rides = db.query(Ride).filter(Ride.user_id == user_id).all()
    return rides

@router.get("/riders/{rider_id}/rides", response_model=List[RideResponse])
def get_rider_rides(rider_id: int, db: Session = Depends(get_db)):
    """Get all rides for a specific rider"""
    rides = db.query(Ride).filter(Ride.rider_id == rider_id).all()
    return rides