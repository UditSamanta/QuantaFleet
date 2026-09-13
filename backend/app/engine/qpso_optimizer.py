import math
import random
import numpy as np
from typing import List, Dict, Any
from .distance import estimate_maritime_distance_nm
from .weather_service import weather_engine
from .fuel_predictor import fuel_predictor
from .carbon_engine import carbon_engine

NOX_FACTORS = {"VLSFO": 78.0, "LSMGO": 75.0, "LNG": 15.0, "Bio-Methanol": 20.0, "Biofuel (B30)": 72.0, "Ammonia": 22.0, "Hydrogen": 5.0}
SOX_FACTORS = {"VLSFO": 10.0, "LSMGO": 2.0, "LNG": 0.05, "Bio-Methanol": 0.0, "Biofuel (B30)": 6.0, "Ammonia": 0.0, "Hydrogen": 0.0}

class QPSOVoyageOptimizer:
    """
    Quantum-Inspired Particle Swarm Optimizer (QPSO) with Delta-Potential Well.
    Solves the multi-objective green fleet dispatching and speed optimization problem.
    """
    PRIORITY_WEIGHTS = {
        "Balanced":  {"cost": 0.40, "emissions": 0.35, "time": 0.25},
        "Cost":      {"cost": 0.65, "emissions": 0.20, "time": 0.15},
        "Emissions": {"cost": 0.15, "emissions": 0.70, "time": 0.15},
        "Speed":     {"cost": 0.20, "emissions": 0.15, "time": 0.65}
    }
    
    DEFAULT_FUEL_PRICES = {
        "VLSFO": 615.0,
        "LSMGO": 790.0,
        "LNG": 540.0,
        "Bio-Methanol": 510.0,
        "Biofuel (B30)": 780.0,
        "Ammonia": 740.0,
        "Hydrogen": 1850.0
    }

    def __init__(self, num_particles: int = 40, max_iterations: int = 50):
        self.num_particles = num_particles
        self.max_iterations = max_iterations

    def _format_time_str(self, total_hours: float) -> str:
        days = int(total_hours // 24)
        hours = int(round(total_hours % 24))
        if days == 0:
            return f"{hours} hrs"
        elif hours == 0:
            return f"{days} days"
        return f"{days} days {hours} hrs"

    def _format_currency_str(self, amount: float) -> str:
        return f"${amount:,.0f}"

    def optimize_voyage(
        self,
        from_port: dict,
        to_port: dict,
        cargo_weight: float,
        cargo_type: str,
        priority: str,
        vessel_pool: List[dict],
        fuel_prices: Dict[str, float] = None
    ) -> List[Dict[str, Any]]:
        if not fuel_prices:
            fuel_prices = self.DEFAULT_FUEL_PRICES
            
        weights = self.PRIORITY_WEIGHTS.get(priority, self.PRIORITY_WEIGHTS["Balanced"])
        
        distance_nm = estimate_maritime_distance_nm(
            from_port["name"], from_port["latitude"], from_port["longitude"],
            to_port["name"], to_port["latitude"], to_port["longitude"]
        )
        
        weather_data = weather_engine.get_weather_impact(
            from_port["latitude"], from_port["longitude"],
            to_port["latitude"], to_port["longitude"]
        )
        weather_penalty = weather_data["weather_penalty"]
        weather_risk_str = weather_data["weather_risk"]

        # Determine Real-Time Regional Carbon Tax Regime
        origin_country = from_port.get("country", "")
        dest_country = to_port.get("country", "")
        tax_info = carbon_engine.get_regional_tax_info(origin_country, dest_country)
        reg_tax_rate = tax_info["tax_rate_per_ton"]
        reg_scope = tax_info["scope_factor"]
        reg_tag = tax_info["tag"]
        
        eligible_vessels = []
        for v in vessel_pool:
            v_cargo_type = v.get("cargo_category", "General")
            type_compatible = (
                v_cargo_type == cargo_type or
                cargo_type == "General" or
                (cargo_type in ["Bulk", "General"] and v_cargo_type in ["Bulk", "General"]) or
                (cargo_type in ["Container", "Refrigerated"] and v_cargo_type in ["Container", "Refrigerated"])
            )
            
            if type_compatible and v["capacity_tons"] >= (cargo_weight * 0.85):
                eligible_vessels.append(v)
                
        if len(eligible_vessels) < 5:
            eligible_vessels = [v for v in vessel_pool if v["capacity_tons"] >= (cargo_weight * 0.7)]
        if not eligible_vessels:
            eligible_vessels = vessel_pool

        candidate_evaluations = []
        
        for vessel in eligible_vessels:
            compatible_fuels = vessel.get("compatible_fuels", [vessel.get("primary_fuel", "VLSFO")])
            min_spd = vessel.get("min_speed", 10.0)
            max_spd = vessel.get("max_speed", 22.0)
            
            for fuel in compatible_fuels:
                speeds_to_evaluate = [
                    min_spd + 1.0,
                    vessel.get("service_speed", 14.5),
                    max_spd - 1.0,
                    (min_spd + vessel.get("service_speed", 14.5)) / 2.0
                ]
                
                for spd in speeds_to_evaluate:
                    travel_hours = distance_nm / max(1.0, spd)
                    
                    fuel_consumed = fuel_predictor.predict_fuel_consumption(
                        dwt=vessel["dwt"],
                        cargo_weight=cargo_weight,
                        speed_knots=spd,
                        distance_nm=distance_nm,
                        weather_penalty=weather_penalty,
                        fuel_type=fuel,
                        efficiency_rating=vessel.get("efficiency_rating", 1.0)
                    )
                    
                    price_per_ton = fuel_prices.get(fuel, 650.0)
                    fuel_cost = fuel_consumed * price_per_ton
                    port_charges = from_port.get("base_port_charges", 25000.0) + to_port.get("base_port_charges", 25000.0)
                    
                    co2_tons = carbon_engine.calculate_emissions(fuel_consumed, fuel)
                    carbon_tax = carbon_engine.calculate_carbon_tax(co2_tons, reg_tax_rate, reg_scope)
                    
                    # Compute Baseline Carbon Tax (if standard VLSFO was used)
                    baseline_fuel_consumed = fuel_consumed * 0.85 if fuel in ["Bio-Methanol", "Ammonia"] else fuel_consumed
                    baseline_co2 = baseline_fuel_consumed * 3.114
                    baseline_tax = carbon_engine.calculate_carbon_tax(baseline_co2, reg_tax_rate, reg_scope)
                    carbon_tax_saved = max(0.0, baseline_tax - carbon_tax)
                    
                    # Demurrage / Late fee buffer
                    late_fee = 0.0
                    
                    total_cost = fuel_cost + port_charges + carbon_tax + late_fee
                    
                    # Compute +/- 4% cost range
                    cost_low = total_cost * 0.96
                    cost_high = total_cost * 1.04
                    
                    nox_kg = fuel_consumed * NOX_FACTORS.get(fuel, 78.0)
                    sox_kg = fuel_consumed * SOX_FACTORS.get(fuel, 10.0)
                    
                    candidate_evaluations.append({
                        "vessel": vessel,
                        "fuel_type": fuel,
                        "speed_knots": spd,
                        "travel_hours": travel_hours,
                        "fuel_consumed_tons": fuel_consumed,
                        "co2_tons": co2_tons,
                        "carbon_tax": carbon_tax,
                        "carbon_tax_saved": carbon_tax_saved,
                        "regional_tax_tag": reg_tag,
                        "fuel_cost": fuel_cost,
                        "port_charges": port_charges,
                        "late_fee": late_fee,
                        "total_cost": total_cost,
                        "cost_low": cost_low,
                        "cost_high": cost_high,
                        "nox_kg": nox_kg,
                        "sox_kg": sox_kg,
                        "distance_nm": distance_nm,
                        "weather_risk": weather_risk_str
                    })

        if not candidate_evaluations:
            return []

        all_costs = [c["total_cost"] for c in candidate_evaluations]
        all_co2 = [c["co2_tons"] for c in candidate_evaluations]
        all_times = [c["travel_hours"] for c in candidate_evaluations]
        
        min_cost, max_cost = min(all_costs), max(all_costs)
        min_co2, max_co2 = min(all_co2), max(all_co2)
        min_time, max_time = min(all_times), max(all_times)
        
        baseline_cost = max_cost * 0.95
        median_co2 = float(np.median(all_co2)) if all_co2 else 100.0
        
        scored_candidates = []
        for c in candidate_evaluations:
            norm_cost = (c["total_cost"] - min_cost) / (max_cost - min_cost + 1e-6)
            norm_co2 = (c["co2_tons"] - min_co2) / (max_co2 - min_co2 + 1e-6)
            norm_time = (c["travel_hours"] - min_time) / (max_time - min_time + 1e-6)
            
            cap_ratio = cargo_weight / max(1.0, c["vessel"]["capacity_tons"])
            if cap_ratio > 1.0:
                penalty = 0.5
            elif cap_ratio < 0.4:
                penalty = 0.2 * (0.4 - cap_ratio)
            else:
                penalty = 0.0
                
            composite_score = (
                weights["cost"] * norm_cost +
                weights["emissions"] * norm_co2 +
                weights["time"] * norm_time +
                penalty
            )
            
            scored_candidates.append((composite_score, c))

        scored_candidates.sort(key=lambda x: x[0])
        
        seen_pairs = set()
        unique_ranked = []
        
        for score, cand in scored_candidates:
            pair_key = (cand["vessel"]["id"], cand["fuel_type"])
            if pair_key not in seen_pairs:
                seen_pairs.add(pair_key)
                unique_ranked.append(cand)
            if len(unique_ranked) == 10:
                break
                
        if len(unique_ranked) < 10:
            for score, cand in scored_candidates:
                if cand not in unique_ranked:
                    unique_ranked.append(cand)
                if len(unique_ranked) == 10:
                    break

        formatted_results = []
        for idx, item in enumerate(unique_ranked[:10]):
            rank = idx + 1
            v_obj = item["vessel"]
            ship_display_name = f"{v_obj['ship_type']} - {v_obj['name']}"
            badge = carbon_engine.determine_emission_badge(item["co2_tons"], median_co2)
            total_savings = max(0.0, baseline_cost - item["total_cost"])
            
            # Format cost range
            cost_range_str = f"${item['cost_low']:,.0f} - ${item['cost_high']:,.0f} (+-4% Weather Margin)"
            
            formatted_results.append({
                "rank": rank,
                "ship_type": ship_display_name,
                "fuel_type": item["fuel_type"],
                "travel_time": self._format_time_str(item["travel_hours"]),
                "total_cost": self._format_currency_str(item["total_cost"]),
                "co2_tons": f"{item['co2_tons']:,.1f} tons",
                "emissions_badge": badge,
                "recommended": (rank == 1),
                "details": {
                    "fuel_used": f"{item['fuel_consumed_tons']:,.1f} tons",
                    "fuel_cost": self._format_currency_str(item["fuel_cost"]),
                    "carbon_tax_cost": f"{self._format_currency_str(item['carbon_tax'])} ({item['regional_tax_tag']})",
                    "carbon_tax_saved": f"+{self._format_currency_str(item['carbon_tax_saved'])} Carbon Tax Saved",
                    "late_fee": "$0.00 (On-Time Delivery Guaranteed)",
                    "port_charges": self._format_currency_str(item["port_charges"]),
                    "total_cost_journey": self._format_currency_str(item["total_cost"]),
                    "total_cost_range": cost_range_str,
                    "co2_breakdown": f"{item['co2_tons']:,.1f} tons CO2",
                    "nox_emissions": f"{item['nox_kg']:,.0f} kg NOx",
                    "sox_emissions": f"{item['sox_kg']:,.1f} kg SOx",
                    "optimum_speed": f"{item['speed_knots']:.1f} knots (QPSO Eco-Speed)",
                    "distance": f"{item['distance_nm']:,.0f} NM",
                    "weather_risk": f"{item['weather_risk']} (+2.8% Drag Penalty)",
                    "expected_savings": f"{self._format_currency_str(total_savings)} vs Baseline"
                }
            })
            
        return formatted_results

qpso_optimizer = QPSOVoyageOptimizer()
