from fastapi import APIRouter
from ..schemas.master_schemas import EmissionCalcRequest, EmissionCalcResponse, TaxCalcRequest, TaxCalcResponse
from ..engine.carbon_engine import carbon_engine

router = APIRouter(prefix="", tags=["Emission & Carbon Tax Engine"])

# IMO Emission Factors
NOX_FACTORS = {"VLSFO": 78.0, "LSMGO": 75.0, "LNG": 15.0, "Bio-Methanol": 20.0, "Biofuel (B30)": 72.0, "Ammonia": 22.0, "Hydrogen": 5.0}
SOX_FACTORS = {"VLSFO": 10.0, "LSMGO": 2.0, "LNG": 0.05, "Bio-Methanol": 0.0, "Biofuel (B30)": 6.0, "Ammonia": 0.0, "Hydrogen": 0.0}

@router.post("/calculate-emission", response_model=EmissionCalcResponse)
def calculate_emission(req: EmissionCalcRequest):
    co2 = carbon_engine.calculate_emissions(req.fuel_consumed_tons, req.fuel_type)
    tax_rate = 85.0
    tax_cost = carbon_engine.calculate_carbon_tax(co2, tax_rate)
    
    nox = req.fuel_consumed_tons * NOX_FACTORS.get(req.fuel_type, 78.0)
    sox = req.fuel_consumed_tons * SOX_FACTORS.get(req.fuel_type, 10.0)
    
    badge = "green" if req.fuel_type in ["Bio-Methanol", "Ammonia", "Hydrogen", "LNG"] else "yellow" if req.fuel_type == "Biofuel (B30)" else "red"
    
    return {
        "fuel_type": req.fuel_type,
        "fuel_consumed_tons": req.fuel_consumed_tons,
        "co2_emissions_tons": round(co2, 2),
        "nox_emissions_kg": round(nox, 1),
        "sox_emissions_kg": round(sox, 1),
        "carbon_tax_rate_per_ton": tax_rate,
        "carbon_tax_total_usd": round(tax_cost, 2),
        "emission_badge": badge
    }

@router.post("/calculate-tax", response_model=TaxCalcResponse)
def calculate_tax(req: TaxCalcRequest):
    rate = req.tax_rate_usd_per_ton or 85.0
    carbon_tax = req.co2_emissions_tons * rate
    port_charges = req.port_charges_usd or 50000.0
    total = req.fuel_cost_usd + carbon_tax + port_charges
    
    share_pct = (carbon_tax / max(1.0, total)) * 100.0
    
    return {
        "co2_emissions_tons": req.co2_emissions_tons,
        "carbon_tax_rate": rate,
        "carbon_tax_cost_usd": round(carbon_tax, 2),
        "fuel_cost_usd": req.fuel_cost_usd,
        "port_charges_usd": port_charges,
        "total_voyage_cost_usd": round(total, 2),
        "carbon_tax_share_pct": round(share_pct, 1)
    }
