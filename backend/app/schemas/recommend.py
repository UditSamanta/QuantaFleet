from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any

class PortItem(BaseModel):
    id: int
    name: str
    code: str
    country: str
    country_code: str
    latitude: float
    longitude: float

class RouteRequest(BaseModel):
    from_port: str = Field(..., description="Departure Port Name or UN/LOCODE")
    to_port: str = Field(..., description="Destination Port Name or UN/LOCODE")
    cargo_weight: float = Field(..., gt=0, description="Cargo Weight in metric tons")
    cargo_type: str = Field(..., description="Cargo category: General / Bulk / Container / Liquid / Refrigerated")
    priority: Optional[Literal["Balanced", "Cost", "Speed", "Emissions"]] = "Balanced"

class SimplifiedDetails(BaseModel):
    fuel_used: str                     # e.g., "3,343.9 tons"
    fuel_cost: str                     # e.g., "$1,705,389"
    carbon_tax_cost: str               # e.g., "$127,908 (EU ETS 50% @ $85/T)"
    carbon_tax_saved: str              # e.g., "+$226,440 Carbon Tax Saved"
    late_fee: str                      # e.g., "$0.00 (On-Time Delivery Guaranteed)"
    port_charges: str                  # e.g., "$71,000"
    total_cost_journey: str            # e.g., "$1,904,305"
    total_cost_range: str              # e.g., "$1.85M - $1.96M (±4% Weather Swell)"
    co2_breakdown: str                 # e.g., "1,504.8 tons CO2"
    nox_emissions: str                 # e.g., "66,878 kg NOx"
    sox_emissions: str                 # e.g., "0.0 kg SOx (Zero-Sulfur)"
    optimum_speed: str                 # e.g., "15.2 knots (Eco-Operating Speed)"
    distance: str                      # e.g., "8,280 NM"
    weather_risk: str                  # e.g., "Moderate Risk (+3.2% Drag Penalty)"
    expected_savings: str              # e.g., "$435,695 vs Baseline"

class RecommendationItem(BaseModel):
    rank: int
    ship_type: str
    fuel_type: str
    travel_time: str
    total_cost: str
    co2_tons: str
    emissions_badge: Literal["green", "yellow", "red"]
    recommended: bool
    details: Optional[SimplifiedDetails] = None

class WeatherSummary(BaseModel):
    wind_speed_knots: float
    wind_speed_kmh: float
    wind_direction: str
    wind_direction_deg: float
    wind_direction_cardinal: str
    visibility_nm: float
    temperature_c: float
    water_temperature_c: Optional[float] = None
    pressure_hpa: float
    pressure_zone: Optional[str] = None
    pressure_badge: Optional[str] = None
    wave_height_m: float
    wave_period_s: Optional[float] = None
    wave_direction_deg: Optional[float] = None
    ocean_current_knots: float
    ocean_current_direction: Optional[str] = None
    weather_risk_score: int
    weather_risk_level: Literal["Low Risk", "Medium Risk", "High Risk"]
    rule_explanation: str
    api_source: Optional[str] = None
    midpoint_coordinates: Dict[str, float]

class RouteGeometry(BaseModel):
    origin: Dict[str, Any]
    destination: Dict[str, Any]
    waypoints: List[List[float]]
    midpoint: Dict[str, float]
    ocean_stations: Optional[List[Dict[str, Any]]] = None

class RecommendationResponse(BaseModel):
    origin_port: str
    destination_port: str
    cargo_weight: str
    cargo_type: str
    priority: str
    weather_summary: Optional[WeatherSummary] = None
    route_geometry: Optional[RouteGeometry] = None
    results: List[RecommendationItem]
