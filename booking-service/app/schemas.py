from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class RideBase(BaseModel):
    user_id: int
    pickup_location: str
    dropoff_location: str

class RideCreate(RideBase):
    pass

class RideUpdate(BaseModel):
    status: str
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ["Pending", "In Progress", "Completed", "Canceled"]
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return v

class RideResponse(RideBase):
    id: int
    rider_id: int
    distance_km: float
    fare_amount: float
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class RideRequest(BaseModel):
    user_id: int
    pickup_location: str
    dropoff_location: str

class RiderMatchResponse(BaseModel):
    rider_id: int
    distance_km: float