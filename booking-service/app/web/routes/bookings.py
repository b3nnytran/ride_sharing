from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.data.database import get_db
from app.data.schemas import RideRequest, RideResponse, RideUpdate
from app.service.booking_service import (
    create_ride_service, get_rides_service, get_ride_service,
    get_user_rides_service, get_rider_rides_service, update_ride_status_service
)

router = APIRouter()

@router.post("/rides/request", response_model=RideResponse)
async def request_ride(ride_request: RideRequest, db: Session = Depends(get_db)):
    """API endpoint to request a ride."""
    ride = await create_ride_service(ride_request, db)
    return ride

@router.get("/rides", response_model=List[RideResponse])
def get_rides(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """API endpoint to get a list of rides."""
    return get_rides_service(db, skip, limit)

@router.get("/rides/{ride_id}", response_model=RideResponse)
def get_ride(ride_id: int, db: Session = Depends(get_db)):
    """API endpoint to get ride details."""
    ride = get_ride_service(ride_id, db)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    return ride

@router.get("/users/{user_id}/rides", response_model=List[RideResponse])
def get_user_rides(user_id: int, db: Session = Depends(get_db)):
    """API endpoint to get a user's rides."""
    return get_user_rides_service(user_id, db)

@router.get("/riders/{rider_id}/rides", response_model=List[RideResponse])
def get_rider_rides(rider_id: int, db: Session = Depends(get_db)):
    """API endpoint to get a rider's rides."""
    return get_rider_rides_service(rider_id, db)

@router.patch("/rides/{ride_id}/status", response_model=RideResponse)
def update_ride_status(ride_id: int, ride_update: RideUpdate, db: Session = Depends(get_db)):
    """API endpoint to update ride status."""
    ride = update_ride_status_service(ride_id, ride_update, db)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    return ride
