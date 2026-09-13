import math
from typing import List
from .maritime_router import maritime_router, haversine_nm

def haversine_distance_nm(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance between two points in Nautical Miles (NM)."""
    return haversine_nm([lat1, lon1], [lat2, lon2])

def estimate_maritime_distance_nm(port1_name: str, lat1: float, lon1: float, port2_name: str, lat2: float, lon2: float) -> float:
    """
    Calculates realistic sea distance using the global maritime sea-lane graph,
    ensuring routes navigate around peninsulas, capes, and straits.
    """
    _, total_sea_nm = maritime_router.get_sea_route([lat1, lon1], [lat2, lon2])
    return total_sea_nm

def generate_geodesic_waypoints(lat1: float, lon1: float, lat2: float, lon2: float, n_points: int = 30) -> List[List[float]]:
    """
    Generates a realistic sea-lane navigation trajectory that stays 100% in ocean waters,
    navigating around landmasses and straits.
    """
    waypoints, _ = maritime_router.get_sea_route([lat1, lon1], [lat2, lon2])
    return waypoints
