from ..config import settings
from typing import Dict, Any, Tuple

class CarbonEngine:
    """
    Computes greenhouse gas emissions (CO2 in tons), Regional Real-Time Carbon Taxes 
    (EU ETS, UK ETS, US ECA, Asia-Pac, IMO Global Levy), and exact financial money savings.
    """
    EMISSION_FACTORS = {
        "VLSFO": 3.114,
        "LSMGO": 3.206,
        "LNG": 2.750,
        "Bio-Methanol": 0.450,
        "Biofuel (B30)": 2.180,
        "Ammonia": 0.050,
        "Hydrogen": 0.000
    }
    
    # Regional Carbon Tax Regimes
    EU_COUNTRIES = {"Netherlands", "Belgium", "Germany", "Spain", "Greece", "France", "Italy", "NL", "BE", "DE", "ES", "GR", "FR", "IT"}
    UK_COUNTRIES = {"United Kingdom", "GB", "UK"}
    NA_COUNTRIES = {"United States", "Canada", "US", "CA"}
    APAC_COUNTRIES = {"Singapore", "China", "Japan", "South Korea", "Hong Kong", "Taiwan", "Malaysia", "SG", "CN", "JP", "KR", "HK", "TW", "MY"}

    @classmethod
    def get_regional_tax_info(cls, origin_country: str, destination_country: str) -> Dict[str, Any]:
        """
        Determines the active real-time regulatory carbon taxation regime and rate for the voyage.
        """
        c1 = origin_country.strip()
        c2 = destination_country.strip()

        is_c1_eu = c1 in cls.EU_COUNTRIES
        is_c2_eu = c2 in cls.EU_COUNTRIES
        
        is_c1_uk = c1 in cls.UK_COUNTRIES
        is_c2_uk = c2 in cls.UK_COUNTRIES
        
        is_c1_na = c1 in cls.NA_COUNTRIES
        is_c2_na = c2 in cls.NA_COUNTRIES
        
        is_c1_apac = c1 in cls.APAC_COUNTRIES
        is_c2_apac = c2 in cls.APAC_COUNTRIES

        if is_c1_eu and is_c2_eu:
            return {
                "region_name": "EU ETS Maritime Directive (Intra-EU 100% Scope)",
                "tax_rate_per_ton": 85.00,
                "scope_factor": 1.00,
                "effective_rate_per_ton": 85.00,
                "tag": "EU ETS @ $85/T"
            }
        elif is_c1_eu or is_c2_eu:
            return {
                "region_name": "EU ETS Maritime Directive (Extra-EU 50% Scope)",
                "tax_rate_per_ton": 85.00,
                "scope_factor": 0.50,
                "effective_rate_per_ton": 42.50,
                "tag": "EU ETS 50% @ $85/T"
            }
        elif is_c1_uk or is_c2_uk:
            return {
                "region_name": "UK ETS Maritime Carbon Scheme",
                "tax_rate_per_ton": 68.00,
                "scope_factor": 0.50,
                "effective_rate_per_ton": 34.00,
                "tag": "UK ETS @ $68/T"
            }
        elif is_c1_na or is_c2_na:
            return {
                "region_name": "North America ECA & CARB Carbon Market",
                "tax_rate_per_ton": 45.00,
                "scope_factor": 0.50,
                "effective_rate_per_ton": 22.50,
                "tag": "US/CA ECA @ $45/T"
            }
        elif is_c1_apac or is_c2_apac:
            return {
                "region_name": "Asia-Pacific Regional Green Carbon Policy",
                "tax_rate_per_ton": 32.00,
                "scope_factor": 0.50,
                "effective_rate_per_ton": 16.00,
                "tag": "APAC Carbon @ $32/T"
            }
        else:
            return {
                "region_name": "IMO Global GHG Net-Zero Carbon Levy Framework",
                "tax_rate_per_ton": 50.00,
                "scope_factor": 0.30,
                "effective_rate_per_ton": 15.00,
                "tag": "IMO Levy @ $50/T"
            }

    @classmethod
    def calculate_emissions(cls, fuel_consumed_tons: float, fuel_type: str) -> float:
        factor = cls.EMISSION_FACTORS.get(fuel_type, 3.114)
        co2_tons = fuel_consumed_tons * factor
        return max(0.0, float(co2_tons))
        
    @classmethod
    def calculate_carbon_tax(cls, co2_tons: float, tax_rate_per_ton: float = None, scope_factor: float = 1.0) -> float:
        rate = tax_rate_per_ton if tax_rate_per_ton is not None else settings.EU_ETS_CARBON_TAX_PER_TON
        return float(co2_tons * rate * scope_factor)

    @classmethod
    def determine_emission_badge(cls, co2_tons: float, benchmark_co2: float) -> str:
        if benchmark_co2 <= 0:
            return "green"
        ratio = co2_tons / benchmark_co2
        if ratio <= 0.65:
            return "green"
        elif ratio <= 1.05:
            return "yellow"
        else:
            return "red"

carbon_engine = CarbonEngine()
