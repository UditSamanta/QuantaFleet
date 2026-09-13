from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class FuelPredictRequest(BaseModel):
    distance_nm: float = Field(..., gt=0, description="Voyage distance in Nautical Miles")
    cargo_weight_tons: float = Field(..., gt=0, description="Cargo weight in metric tons")
    speed_knots: float = Field(..., gt=5, lt=30, description="Operating speed in knots")
    wind_speed_knots: Optional[float] = 12.0
    wave_height_m: Optional[float] = 1.5
    visibility_nm: Optional[float] = 10.0
    fuel_type: str = Field(default="VLSFO", description="Fuel: VLSFO, LNG, Bio-Methanol, Ammonia, Hydrogen, etc.")
    ship_type: str = Field(default="Container - Panamax (5,000 TEU)")
    dwt: Optional[float] = 65000.0
    model_choice: Optional[str] = "XGBoost Regressor"  # "XGBoost Regressor", "Random Forest Regressor", "Linear Regression"

class FuelPredictResponse(BaseModel):
    predicted_fuel_consumed_tons: float
    model_used: str
    model_r2_score: float
    daily_fuel_rate_tons_per_day: float
    total_travel_hours: float
    estimated_fuel_cost_usd: float
    estimated_co2_emissions_tons: float
    all_models_comparison: Dict[str, float]

class EmissionCalcRequest(BaseModel):
    fuel_consumed_tons: float = Field(..., gt=0)
    fuel_type: str = Field(default="VLSFO")

class EmissionCalcResponse(BaseModel):
    fuel_type: str
    fuel_consumed_tons: float
    co2_emissions_tons: float
    nox_emissions_kg: float
    sox_emissions_kg: float
    carbon_tax_rate_per_ton: float
    carbon_tax_total_usd: float
    emission_badge: str

class TaxCalcRequest(BaseModel):
    co2_emissions_tons: float = Field(..., ge=0)
    fuel_cost_usd: float = Field(..., ge=0)
    port_charges_usd: Optional[float] = 50000.0
    tax_rate_usd_per_ton: Optional[float] = 85.0

class TaxCalcResponse(BaseModel):
    co2_emissions_tons: float
    carbon_tax_rate: float
    carbon_tax_cost_usd: float
    fuel_cost_usd: float
    port_charges_usd: float
    total_voyage_cost_usd: float
    carbon_tax_share_pct: float

class DashboardKPIs(BaseModel):
    total_fleet_vessels: int
    active_voyages_count: int
    total_fuel_cost_ytd_usd: str
    total_carbon_tax_ytd_usd: str
    total_co2_emissions_ytd_tons: str
    average_fleet_utilization_pct: float
    expected_green_savings_usd: str
    green_fuel_adoption_pct: float
    fuel_trend: List[Dict[str, Any]]
    emission_trend: List[Dict[str, Any]]
    cost_breakdown: List[Dict[str, Any]]
    vessel_type_distribution: List[Dict[str, Any]]

class AIInsightItem(BaseModel):
    id: str
    category: str  # Speed Advisory, Vessel Switching, Weather Route, Carbon Tax
    title: str
    description: str
    potential_savings: str
    emission_impact: str
    severity: str  # 'high', 'medium', 'low'
