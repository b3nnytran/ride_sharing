from fastapi import APIRouter, Depends, HTTPException, status
from app.distance_matrix import DistanceMatrixService
from app.schemas import MatchingRequest, MatchingResponse

router = APIRouter()

@router.post("/match", response_model=MatchingResponse)
async def match_rider(request: MatchingRequest, distance_service: DistanceMatrixService = Depends()):
    """Find the nearest available rider for a user"""
    result = await distance_service.find_nearest_rider(request.user_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No available riders found"
        )
    
    rider_id, distance = result
    return {"rider_id": rider_id, "distance_km": distance}