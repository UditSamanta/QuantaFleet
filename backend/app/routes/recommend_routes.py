from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
import json

from ..database import get_db
from ..models.user import User
from ..models.maritime import Port, Vessel, FuelPrice
from ..schemas.recommend import RouteRequest, RecommendationResponse
from ..auth.deps import get_current_user
from ..engine.qpso_optimizer import qpso_optimizer
from ..engine.weather_service import weather_engine
from ..engine.distance import generate_geodesic_waypoints
from ..engine.presentation_generator import generate_voyage_pptx

router = APIRouter(prefix="", tags=["Recommendations & Reports"])

PORT_ALIASES = {
    "mumbai": "Jawaharlal Nehru Port (JNPT)",
    "port of mumbai": "Jawaharlal Nehru Port (JNPT)",
    "bombay": "Jawaharlal Nehru Port (JNPT)",
    "jnpt": "Jawaharlal Nehru Port (JNPT)",
    "chennai": "Port of Chennai",
    "madras": "Port of Chennai",
    "singapore": "Port of Singapore",
    "rotterdam": "Port of Rotterdam",
    "shanghai": "Port of Shanghai",
    "dubai": "Port of Jebel Ali",
    "jebel ali": "Port of Jebel Ali",
    "los angeles": "Port of Los Angeles",
    "new york": "Port of New York & New Jersey",
    "houston": "Port of Houston",
    "santos": "Port of Santos",
    "hamburg": "Port of Hamburg",
    "antwerp": "Port of Antwerp-Bruges",
    "busan": "Port of Busan",
    "tokyo": "Port of Tokyo",
}

def resolve_port(db: Session, query_str: str) -> Optional[Port]:
    q = query_str.strip().lower()
    
    # Check aliases
    for alias_key, full_name in PORT_ALIASES.items():
        if alias_key in q or q in alias_key:
            port = db.query(Port).filter(Port.name.ilike(f"%{full_name}%")).first()
            if port:
                return port
                
    # Direct search by name, code or country
    port = db.query(Port).filter(
        (Port.name.ilike(f"%{query_str.strip()}%")) | (Port.code.ilike(query_str.strip()))
    ).first()
    
    return port

@router.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(
    req: RouteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from_port = resolve_port(db, req.from_port)
    to_port = resolve_port(db, req.to_port)
    
    if not from_port:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Origin port '{req.from_port}' not found in database."
        )
        
    if not to_port:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Destination port '{req.to_port}' not found in database."
        )
        
    if from_port.id == to_port.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Origin and Destination ports cannot be identical."
        )

    vessels = db.query(Vessel).all()
    vessel_pool = [
        {
            "id": v.id,
            "name": v.name,
            "ship_type": v.ship_type,
            "cargo_category": v.cargo_category,
            "dwt": v.dwt,
            "capacity_tons": v.capacity_tons,
            "primary_fuel": v.primary_fuel,
            "compatible_fuels": v.compatible_fuels or [v.primary_fuel],
            "service_speed": v.service_speed,
            "min_speed": v.min_speed,
            "max_speed": v.max_speed,
            "efficiency_rating": v.efficiency_rating
        }
        for v in vessels
    ]
    
    prices_query = db.query(FuelPrice).all()
    fuel_prices = {fp.fuel_type: fp.price_per_ton for fp in prices_query}

    from_port_dict = {
        "name": from_port.name,
        "code": from_port.code,
        "country": from_port.country,
        "latitude": from_port.latitude,
        "longitude": from_port.longitude,
        "base_port_charges": from_port.base_port_charges
    }
    to_port_dict = {
        "name": to_port.name,
        "code": to_port.code,
        "country": to_port.country,
        "latitude": to_port.latitude,
        "longitude": to_port.longitude,
        "base_port_charges": to_port.base_port_charges
    }
    
    # 1. Run QPSO Voyage Optimization with realistic sea distance
    ranked_results = qpso_optimizer.optimize_voyage(
        from_port=from_port_dict,
        to_port=to_port_dict,
        cargo_weight=req.cargo_weight,
        cargo_type=req.cargo_type,
        priority=req.priority or "Balanced",
        vessel_pool=vessel_pool,
        fuel_prices=fuel_prices
    )
    
    if not ranked_results:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No eligible vessel configuration could be found for the given cargo weight and specifications."
        )

    # 2. Compute 100% Oceanic Navigation Sea Waypoints (Around landmasses, straits, capes)
    waypoints = generate_geodesic_waypoints(
        from_port.latitude, from_port.longitude,
        to_port.latitude, to_port.longitude,
        n_points=32
    )

    # Midpoint placed directly along the sea navigation corridor
    mid_idx = len(waypoints) // 2
    mid_point = {
        "lat": round(waypoints[mid_idx][0], 4),
        "lng": round(waypoints[mid_idx][1], 4)
    }

    # 3. Compute Metocean Weather Telemetry at Sea Waypoint
    weather_data = weather_engine.get_weather_impact(
        mid_point["lat"], mid_point["lng"],
        mid_point["lat"], mid_point["lng"]
    )

    # 4. Generate Multi-Station Oceanic Monitoring Stations along the voyage
    ocean_stations = weather_engine.generate_route_ocean_stations(waypoints)

    route_geom = {
        "origin": from_port_dict,
        "destination": to_port_dict,
        "waypoints": waypoints,
        "midpoint": mid_point,
        "ocean_stations": ocean_stations
    }

    return {
        "origin_port": f"{from_port.name} ({from_port.country})",
        "destination_port": f"{to_port.name} ({to_port.country})",
        "cargo_weight": f"{req.cargo_weight:,.0f} tons",
        "cargo_type": req.cargo_type,
        "priority": req.priority or "Balanced",
        "weather_summary": weather_data,
        "route_geometry": route_geom,
        "results": ranked_results
    }

@router.get("/download-ppt")
def download_master_ppt():
    """Generates and serves the SIH master pitch presentation (.pptx)"""
    pptx_stream = generate_voyage_pptx()
    filename = "QuantumFleet_SIH26138_Executive_PitchDeck.pptx"
    return StreamingResponse(
        pptx_stream,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.post("/download-voyage-ppt")
def download_voyage_custom_ppt(data: dict):
    """Generates and serves a customized presentation (.pptx) for the active voyage results"""
    pptx_stream = generate_voyage_pptx(data)
    filename = "QuantumFleet_Voyage_Optimization_Report.pptx"
    return StreamingResponse(
        pptx_stream,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
