from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from app.data.database import get_db
from app.data.schemas import UserCreate, UserResponse, Token
from app.service.user_service import (
    register_user_service, authenticate_user_service,
    generate_access_token, get_all_users_service, get_user_by_id_service
)
from app.data.security import get_current_user

router = APIRouter()

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    new_user = register_user_service(user, db)
    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return new_user

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""
    user = authenticate_user_service(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect phone number or password")
    
    access_token = generate_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserResponse)
def get_current_user_profile(current_user: UserResponse = Depends(get_current_user)):
    """Get current authenticated user profile"""
    return current_user

@router.get("/users", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    """Get list of users (Requires authentication)"""
    return get_all_users_service(db, skip, limit)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    """Get user details by ID"""
    user = get_user_by_id_service(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
