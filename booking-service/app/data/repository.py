from sqlalchemy.orm import Session
from app.data.models import Ride

def create_ride(db: Session, ride: Ride) -> Ride:
    """Save a new ride to the database."""
    db.add(ride)
    db.commit()
    db.refresh(ride)
    return ride

def get_rides(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all rides."""
    return db.query(Ride).offset(skip).limit(limit).all()

def get_ride(db: Session, ride_id: int):
    """Retrieve a ride by ID."""
    return db.query(Ride).filter(Ride.id == ride_id).first()

def get_user_rides(db: Session, user_id: int):
    """Retrieve all rides for a specific user."""
    return db.query(Ride).filter(Ride.user_id == user_id).all()

def get_rider_rides(db: Session, rider_id: int):
    """Retrieve all rides for a specific rider."""
    return db.query(Ride).filter(Ride.rider_id == rider_id).all()

def update_ride_status(db: Session, ride_id: int, status: str):
    """Update the status of a ride."""
    ride = db.query(Ride).filter(Ride.id == ride_id).first()
    if ride:
        ride.status = status
        db.commit()
        db.refresh(ride)
    return ride
