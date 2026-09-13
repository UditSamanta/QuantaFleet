from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.maritime import Port
from ..schemas.recommend import PortItem

router = APIRouter(prefix="/ports", tags=["Ports"])

@router.get("", response_model=List[PortItem])
def list_ports(
    search: Optional[str] = Query(None, description="Search term for port name, code, or country"),
    db: Session = Depends(get_db)
):
    query = db.query(Port)
    if search:
        s = f"%{search.strip()}%"
        query = query.filter(
            (Port.name.ilike(s)) | 
            (Port.code.ilike(s)) | 
            (Port.country.ilike(s))
        )
    ports = query.order_by(Port.name.asc()).all()
    return ports
