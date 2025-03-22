from math import radians, cos, sin, sqrt, atan2
from typing import List, Dict


# Haversine formula to calculate the distance between two lat/long points
def haversine(hospital_lat, hospital_lon, user_lat, user_long):
    R = 6371  # Earth's radius in kilometers
    hospital_lat, hospital_lon, user_lat, user_long = map(radians, [hospital_lat, hospital_lon, user_lat, user_long])

    dlat = user_lat - hospital_lat
    dlon = user_long - hospital_lon
    a = sin(dlat/2)**2 + cos(hospital_lat) * cos(user_lat) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c  # Distance in km

# Function to find the nearest users to a hospital
def find_nearest_users(request_lat: float, request_long: float, users: List[Dict], max_distance: float = 10):

    nearby_users = []
    
    for user in users:
        distance = haversine(request_lat, request_long, user["lat"], user["long"])
        if distance <= max_distance:  # Only consider users within the given radius (e.g., 10 km)
            nearby_users.append({**user, "distance": round(distance, 2)})
    print(sorted(nearby_users, key=lambda x: x["distance"]))
    return sorted(nearby_users, key=lambda x: x["distance"])  # Sort by nearest users

