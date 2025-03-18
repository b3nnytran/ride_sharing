from sqlalchemy.orm import Session
from app.data.models import User

def create_user(db: Session, user: User) -> User:
    """Save a new user to the database."""
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_phone(db: Session, phone_number: str):
    """Retrieve a user by phone number."""
    return db.query(User).filter(User.phone_number == phone_number).first()

def get_user_by_id(db: Session, user_id: int):
    """Retrieve a user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all users."""
    return db.query(User).offset(skip).limit(limit).all()
