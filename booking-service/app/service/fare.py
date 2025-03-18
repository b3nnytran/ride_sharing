def calculate_fare(distance_km: float) -> float:
    """
    Calculate the fare based on the distance using an incremental tiered pricing model.

    Distance-based pricing model:
    - First 1 km → 10,000 VND/km
    - Next 3 km (2-4 km) → 15,000 VND/km
    - Remaining distance (>4 km) → 12,000 VND/km
    """
    fare = 0

    # First 1 km
    if distance_km > 0:
        first_km = min(distance_km, 1)
        fare += first_km * 10000
        distance_km -= first_km

    # Next 3 km (2-4 km)
    if distance_km > 0:
        next_3_km = min(distance_km, 3)
        fare += next_3_km * 15000
        distance_km -= next_3_km

    # Remaining distance (>4 km)
    if distance_km > 0:
        fare += distance_km * 12000

    return fare
