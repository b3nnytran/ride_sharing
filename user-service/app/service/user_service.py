from sqlalchemy.orm import Session
from datetime import timedelta
from app.data.models import User
from app.data.schemas import UserCreate, UserResponse
from app.data.repository import (
    create_user as create_user_repo,
    get_user_by_phone as get_user_by_phone_repo,
    get_user_by_id as get_user_by_id_repo,
    get_all_users as get_all_users_repo
)
from app.data.security import (
    get_password_hash, authenticate_user, create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

def register_user_service(user: UserCreate, db: Session) -> UserResponse:
    """Register a new user after checking if phone number exists."""
    existing_user = get_user_by_phone_repo(db, user.phone_number)
    if existing_user:
        return None  # Handle this in the API layer
    
    hashed_password = get_password_hash(user.password)
    db_user = User(name=user.name, phone_number=user.phone_number, password_hash=hashed_password)
    return create_user_repo(db, db_user)

def authenticate_user_service(phone_number: str, password: str, db: Session):
    """Authenticate a user."""
    return authenticate_user(db, phone_number, password)

def generate_access_token(user_id: int):
    """Generate an access token for an authenticated user."""
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data={"sub": str(user_id)}, expires_delta=access_token_expires)

def get_all_users_service(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all users from the database."""
    return get_all_users_repo(db, skip, limit)

def get_user_by_id_service(user_id: int, db: Session):
    """Retrieve a single user by ID."""
    return get_user_by_id_repo(db, user_id)
