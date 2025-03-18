from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
import re

class RiderBase(BaseModel):
    rider_name: str
    vehicle_type: str
    license_plate: str
    
    @validator('license_plate')
    def validate_license_plate(cls, v):
        # Simple validation for license plate format
        if not re.match(r'^[A-Z0-9-]{5,10}$', v):
            raise ValueError('Invalid license plate format. Must be 5-10 alphanumeric characters or hyphens.')
        return v

class RiderCreate(RiderBase):
    pass

class RiderUpdate(BaseModel):
    vehicle_type: Optional[str] = None
    license_plate: Optional[str] = None
    status: Optional[str] = None
    
    @validator('status')
    def validate_status(cls, v):
        if v not in ["Available", "Busy"]:
            raise ValueError('Status must be either "Available" or "Busy"')
        return v

class RiderResponse(RiderBase):
    id: int
    rider_name: str
    rating: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class DistanceMatrixBase(BaseModel):
    rider_id: int
    distance_km: float

class DistanceMatrixCreate(DistanceMatrixBase):
    pass

class DistanceMatrixResponse(DistanceMatrixBase):
    id: int
    
    class Config:
        from_attributes = True

class NearestRiderRequest(BaseModel):
    rider_name: str

class NearestRiderResponse(BaseModel):
    rider_id: int
    distance_km: float