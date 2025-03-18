import os
import httpx
from fastapi import HTTPException, status
from app.data.schemas import RiderMatchResponse

RIDE_MATCHING_SERVICE_URL = os.getenv("RIDE_MATCHING_SERVICE_URL", "http://ride-matching-service:8004")

async def find_nearest_rider(user_id: int) -> RiderMatchResponse:
    """Gọi đến Ride Matching Service để tìm tài xế gần nhất."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{RIDE_MATCHING_SERVICE_URL}/api/v1/match",
                json={"user_id": user_id}
            )
            response.raise_for_status()
            match_result = response.json()
            return RiderMatchResponse(**match_result)
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Error finding nearest rider: {str(e)}"
            )
