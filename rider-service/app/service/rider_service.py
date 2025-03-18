from sqlalchemy.orm import Session
from app.data.models import Rider, DistanceMatrix
from app.data.schemas import RiderCreate, RiderUpdate, DistanceMatrixCreate
from app.data.repository import (
    create_rider as create_rider_repo,
    get_rider_by_user_id as get_rider_by_user_id_repo,
    get_rider_by_id as get_rider_by_id_repo,
    get_all_riders as get_all_riders_repo,
    update_rider as update_rider_repo,
    create_distance_entry as create_distance_entry_repo
)

def create_rider_service(rider: RiderCreate, db: Session):
    """Register a new rider after checking uniqueness."""
    if get_rider_by_user_id_repo(db, rider.rider_name):
        return None  # Handle in API layer
    
    db_rider = Rider(**rider.dict())
    return create_rider_repo(db, db_rider)

def get_rider_service(rider_id: int, db: Session):
    """Retrieve a specific rider."""
    return get_rider_by_id_repo(db, rider_id)

def get_all_riders_service(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all riders."""
    return get_all_riders_repo(db, skip, limit)

def update_rider_service(rider_id: int, rider_update: RiderUpdate, db: Session):
    """Update rider details."""
    return update_rider_repo(db, rider_id, rider_update.dict(exclude_unset=True))

def create_distance_entry_service(entry: DistanceMatrixCreate, db: Session):
    """Create or update a distance entry."""
    db_entry = DistanceMatrix(**entry.dict())
    return create_distance_entry_repo(db, db_entry)
