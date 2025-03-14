def calculate_fare(distance_km: float) -> float:
    """
    Calculate the fare based on the distance using a tiered pricing model.
    
    Distance-based pricing model:
    - 1 km → 10k/km
    - 2-4 km → 15k/km
    - More than 4 km → 12k/km
    """
    if distance_km <= 1:
        return distance_km * 10000
    elif 1 < distance_km <= 4:
        return distance_km * 15000
    else:  # distance_km > 4
        return distance_km * 12000