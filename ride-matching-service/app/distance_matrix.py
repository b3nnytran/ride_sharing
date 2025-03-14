import os
import httpx
import random
from typing import Dict, List, Optional, Tuple

class DistanceMatrixService:
    def __init__(self):
        self.rider_service_url = os.getenv("RIDER_SERVICE_URL", "http://rider-service:8002")
        self.distance_matrix = {
            # Pre-defined distance matrix as specified in the requirements
            (1, 1): 8.0, (1, 2): 5.0, (1, 3): 6.0, (1, 4): 2.0, (1, 5): 7.0,
            (2, 1): 3.0, (2, 2): 9.0, (2, 3): 4.0, (2, 4): 6.0, (2, 5): 1.0,
            (3, 1): 5.0, (3, 2): 2.0, (3, 3): 8.0, (3, 4): 7.0, (3, 5): 4.0,
            (4, 1): 6.0, (4, 2): 10.0, (4, 3): 3.0, (4, 4): 1.0, (4, 5): 9.0,
            (5, 1): 7.0, (5, 2): 4.0, (5, 3): 2.0, (5, 4): 9.0, (5, 5): 5.0
        }
    
    def get_distance(self, user_id: int, rider_id: int) -> float:
        """Get the distance between a user and a rider"""
        return self.distance_matrix.get((user_id, rider_id), random.uniform(1.0, 10.0))
    
    async def get_available_riders(self) -> List[Dict]:
        """Get list of available riders from the Rider Service"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.rider_service_url}/api/v1/riders")
            response.raise_for_status()
            riders = response.json()
            return [rider for rider in riders if rider["status"] == "Available"]
    
    async def find_nearest_rider(self, user_id: int) -> Optional[Tuple[int, float]]:
        """Find the nearest available rider for a user"""
        available_riders = await self.get_available_riders()
        
        if not available_riders:
            return None
        
        # Calculate distances to all available riders
        distances = []
        for rider in available_riders:
            rider_id = rider["id"]
            distance = self.get_distance(user_id, rider_id)
            distances.append((rider_id, distance))
        
        # Find the minimum distance
        if not distances:
            return None
        
        min_distance = min(distances, key=lambda x: x[1])
        
        # Find all riders with the minimum distance
        closest_riders = [d for d in distances if d[1] == min_distance[1]]
        
        # If multiple riders have the same distance, choose one randomly
        if len(closest_riders) > 1:
            return random.choice(closest_riders)
        return closest_riders[0]