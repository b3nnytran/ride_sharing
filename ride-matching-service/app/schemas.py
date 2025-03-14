from pydantic import BaseModel

class MatchingRequest(BaseModel):
    user_id: int

class MatchingResponse(BaseModel):
    rider_id: int
    distance_km: float