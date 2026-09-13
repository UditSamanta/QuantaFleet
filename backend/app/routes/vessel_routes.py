from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.maritime import Vessel

router = APIRouter(prefix="/vessels", tags=["Fleet Management"])

@router.get("")
def list_vessels(
    search: Optional[str] = Query(None, description="Search vessel by name, IMO, or type"),
    category: Optional[str] = Query(None, description="Bulk, Container, Liquid, General, Refrigerated"),
    fuel: Optional[str] = Query(None, description="Fuel type filter"),
    db: Session = Depends(get_db)
):
    query = db.query(Vessel)
    if search:
        s = f"%{search.strip()}%"
        query = query.filter(
            (Vessel.name.ilike(s)) | (Vessel.imo_number.ilike(s)) | (Vessel.ship_type.ilike(s))
        )
    if category and category != "All":
        query = query.filter(Vessel.cargo_category == category)
    if fuel and fuel != "All":
        query = query.filter(Vessel.primary_fuel == fuel)
        
    vessels = query.order_by(Vessel.dwt.desc()).all()
    
    return [
        {
            "id": v.id,
            "imo_number": v.imo_number,
            "mmsi": v.mmsi,
            "name": v.name,
            "ship_type": v.ship_type,
            "cargo_category": v.cargo_category,
            "dwt": v.dwt,
            "capacity_tons": v.capacity_tons,
            "primary_fuel": v.primary_fuel,
            "compatible_fuels": v.compatible_fuels or [v.primary_fuel],
            "service_speed": v.service_speed,
            "year_built": v.year_built,
            "flag_country": v.flag_country,
            "efficiency_rating": v.efficiency_rating
        }
        for v in vessels
    ]
