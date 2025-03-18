from sqlalchemy.orm import Session
from app.data.models import Ride
from app.data.schemas import RideRequest, RideResponse, RideUpdate
from app.service.fare import calculate_fare
from app.data.repository import (
    create_ride as create_ride_repo,
    get_rides as get_rides_repo,
    get_ride as get_ride_repo,
    get_user_rides as get_user_rides_repo,
    get_rider_rides as get_rider_rides_repo,
    update_ride_status as update_ride_status_repo,
)
import httpx
import os

RIDE_MATCHING_SERVICE_URL = os.getenv("RIDE_MATCHING_SERVICE_URL", "http://ride-matching-service:8004")

async def create_ride_service(ride_request: RideRequest, db: Session) -> RideResponse:
    """Request a ride by finding the nearest available rider."""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{RIDE_MATCHING_SERVICE_URL}/api/v1/match", json={"user_id": ride_request.user_id})
        response.raise_for_status()
        match_result = response.json()

    rider_id = match_result["rider_id"]
    distance_km = match_result["distance_km"]
    fare_amount = calculate_fare(distance_km)

    new_ride = Ride(
        user_id=ride_request.user_id,
        rider_id=rider_id,
        pickup_location=ride_request.pickup_location,
        dropoff_location=ride_request.dropoff_location,
        distance_km=distance_km,
        fare_amount=fare_amount,
        status="Pending"
    )

    return create_ride_repo(db, new_ride)

def get_rides_service(db: Session, skip: int = 0, limit: int = 100):
    """Get all rides."""
    return get_rides_repo(db, skip, limit)

def get_ride_service(ride_id: int, db: Session):
    """Get a specific ride."""
    return get_ride_repo(db, ride_id)

def get_user_rides_service(user_id: int, db: Session):
    """Get all rides for a specific user."""
    return get_user_rides_repo(db, user_id)

def get_rider_rides_service(rider_id: int, db: Session):
    """Get all rides for a specific rider."""
    return get_rider_rides_repo(db, rider_id)

def update_ride_status_service(ride_id: int, ride_update: RideUpdate, db: Session):
    """Update the status of a ride."""
    return update_ride_status_repo(db, ride_id, ride_update.status)
