from sqlalchemy.orm import Session
from app.data.models import Rider, DistanceMatrix

def create_rider(db: Session, rider: Rider) -> Rider:
    """Save a new rider to the database."""
    db.add(rider)
    db.commit()
    db.refresh(rider)
    return rider

def get_rider_by_user_id(db: Session, rider_name: str):
    """Retrieve a rider by user_id."""
    return db.query(Rider).filter(Rider.rider_name == rider_name).first()

def get_rider_by_id(db: Session, rider_id: int):
    """Retrieve a rider by ID."""
    return db.query(Rider).filter(Rider.id == rider_id).first()

def get_all_riders(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all riders."""
    return db.query(Rider).offset(skip).limit(limit).all()

def update_rider(db: Session, rider_id: int, updates: dict):
    """Update rider details."""
    db_rider = db.query(Rider).filter(Rider.id == rider_id).first()
    if db_rider:
        for key, value in updates.items():
            setattr(db_rider, key, value)
        db.commit()
        db.refresh(db_rider)
    return db_rider

def create_distance_entry(db: Session, entry: DistanceMatrix):
    """Save or update distance entry."""
    existing_entry = db.query(DistanceMatrix).filter(
        DistanceMatrix.user_id == entry.user_id,
        DistanceMatrix.rider_id == entry.rider_id
    ).first()
    
    if existing_entry:
        existing_entry.distance_km = entry.distance_km
        db.commit()
        db.refresh(existing_entry)
        return existing_entry

    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
