from sqlalchemy.orm import Session
from ..models.user import User
from ..models.maritime import Vessel, Port, EmissionFactor, FuelPrice
from ..auth.security import get_password_hash

PORTS_SEED = [
    {"name": "Port of Singapore", "code": "SGSIN", "country": "Singapore", "country_code": "SG", "latitude": 1.290270, "longitude": 103.851959, "base_port_charges": 32000.0, "congestion_level": "Moderate"},
    {"name": "Port of Shanghai", "code": "CNSHA", "country": "China", "country_code": "CN", "latitude": 31.230416, "longitude": 121.473701, "base_port_charges": 38000.0, "congestion_level": "High"},
    {"name": "Port of Ningbo-Zhoushan", "code": "CNNGB", "country": "China", "country_code": "CN", "latitude": 29.8683, "longitude": 121.5440, "base_port_charges": 34000.0, "congestion_level": "Moderate"},
    {"name": "Port of Shenzhen", "code": "CNSZX", "country": "China", "country_code": "CN", "latitude": 22.5431, "longitude": 114.0579, "base_port_charges": 33000.0, "congestion_level": "Moderate"},
    {"name": "Port of Busan", "code": "KRPUS", "country": "South Korea", "country_code": "KR", "latitude": 35.1796, "longitude": 129.0756, "base_port_charges": 28000.0, "congestion_level": "Low"},
    {"name": "Port of Hong Kong", "code": "HKHKG", "country": "Hong Kong", "country_code": "HK", "latitude": 22.3193, "longitude": 114.1694, "base_port_charges": 31000.0, "congestion_level": "Moderate"},
    {"name": "Port of Tokyo", "code": "JPTYO", "country": "Japan", "country_code": "JP", "latitude": 35.6762, "longitude": 139.6503, "base_port_charges": 35000.0, "congestion_level": "Low"},
    {"name": "Port of Yokohama", "code": "JPYOK", "country": "Japan", "country_code": "JP", "latitude": 35.4437, "longitude": 139.6380, "base_port_charges": 32000.0, "congestion_level": "Low"},
    {"name": "Port of Klang", "code": "MYPKG", "country": "Malaysia", "country_code": "MY", "latitude": 3.0000, "longitude": 101.4000, "base_port_charges": 24000.0, "congestion_level": "Moderate"},
    {"name": "Port of Tanjung Pelepas", "code": "MYTPP", "country": "Malaysia", "country_code": "MY", "latitude": 1.3620, "longitude": 103.5490, "base_port_charges": 23000.0, "congestion_level": "Low"},
    {"name": "Port of Kaohsiung", "code": "TWKHH", "country": "Taiwan", "country_code": "TW", "latitude": 22.6273, "longitude": 120.3014, "base_port_charges": 27000.0, "congestion_level": "Low"},
    {"name": "Port of Sydney", "code": "AUSYD", "country": "Australia", "country_code": "AU", "latitude": -33.8688, "longitude": 151.2093, "base_port_charges": 36000.0, "congestion_level": "Low"},
    {"name": "Port of Melbourne", "code": "AUMEL", "country": "Australia", "country_code": "AU", "latitude": -37.8136, "longitude": 144.9631, "base_port_charges": 34000.0, "congestion_level": "Low"},
    {"name": "Jawaharlal Nehru Port (JNPT Mumbai)", "code": "INNSA", "country": "India", "country_code": "IN", "latitude": 18.9499, "longitude": 72.9515, "base_port_charges": 22000.0, "congestion_level": "Moderate"},
    {"name": "Port of Chennai", "code": "INMAA", "country": "India", "country_code": "IN", "latitude": 13.0827, "longitude": 80.2707, "base_port_charges": 20000.0, "congestion_level": "Moderate"},
    {"name": "Port of Mundra", "code": "INMUN", "country": "India", "country_code": "IN", "latitude": 22.8396, "longitude": 69.7042, "base_port_charges": 21000.0, "congestion_level": "Low"},
    {"name": "Port of Colombo", "code": "LKCMB", "country": "Sri Lanka", "country_code": "LK", "latitude": 6.9271, "longitude": 79.8612, "base_port_charges": 25000.0, "congestion_level": "Moderate"},
    {"name": "Port of Jebel Ali (Dubai)", "code": "AEJEA", "country": "United Arab Emirates", "country_code": "AE", "latitude": 25.0113, "longitude": 55.0612, "base_port_charges": 30000.0, "congestion_level": "Moderate"},
    {"name": "Port of Salalah", "code": "OMSLL", "country": "Oman", "country_code": "OM", "latitude": 16.9442, "longitude": 54.0041, "base_port_charges": 23000.0, "congestion_level": "Low"},
    {"name": "King Abdullah Port", "code": "SAKAP", "country": "Saudi Arabia", "country_code": "SA", "latitude": 22.5367, "longitude": 39.0967, "base_port_charges": 26000.0, "congestion_level": "Low"},
    {"name": "Port of Rotterdam", "code": "NLRTM", "country": "Netherlands", "country_code": "NL", "latitude": 51.9244, "longitude": 4.4777, "base_port_charges": 39000.0, "congestion_level": "Moderate"},
    {"name": "Port of Antwerp-Bruges", "code": "BEANR", "country": "Belgium", "country_code": "BE", "latitude": 51.2194, "longitude": 4.4025, "base_port_charges": 36000.0, "congestion_level": "Moderate"},
    {"name": "Port of Hamburg", "code": "DEHAM", "country": "Germany", "country_code": "DE", "latitude": 53.5511, "longitude": 9.9937, "base_port_charges": 37000.0, "congestion_level": "Moderate"},
    {"name": "Port of Valencia", "code": "ESVLC", "country": "Spain", "country_code": "ES", "latitude": 39.4699, "longitude": -0.3763, "base_port_charges": 29000.0, "congestion_level": "Low"},
    {"name": "Port of Algeciras", "code": "ESALG", "country": "Spain", "country_code": "ES", "latitude": 36.1408, "longitude": -5.4562, "base_port_charges": 28000.0, "congestion_level": "Low"},
    {"name": "Port of Piraeus (Athens)", "code": "GRPIR", "country": "Greece", "country_code": "GR", "latitude": 37.9430, "longitude": 23.6470, "base_port_charges": 27000.0, "congestion_level": "Moderate"},
    {"name": "Port of Felixstowe", "code": "GBFXT", "country": "United Kingdom", "country_code": "GB", "latitude": 51.9634, "longitude": 1.3511, "base_port_charges": 33000.0, "congestion_level": "Moderate"},
    {"name": "Port of Le Havre", "code": "FRLEH", "country": "France", "country_code": "FR", "latitude": 49.4944, "longitude": 0.1079, "base_port_charges": 31000.0, "congestion_level": "Low"},
    {"name": "Port of Genoa", "code": "ITGOA", "country": "Italy", "country_code": "IT", "latitude": 44.4056, "longitude": 8.9463, "base_port_charges": 30000.0, "congestion_level": "Low"},
    {"name": "Port of Los Angeles", "code": "USLAX", "country": "United States", "country_code": "US", "latitude": 33.7432, "longitude": -118.2673, "base_port_charges": 42000.0, "congestion_level": "High"},
    {"name": "Port of Long Beach", "code": "USLGB", "country": "United States", "country_code": "US", "latitude": 33.7701, "longitude": -118.1937, "base_port_charges": 41000.0, "congestion_level": "Moderate"},
    {"name": "Port of New York and New Jersey", "code": "USNYC", "country": "United States", "country_code": "US", "latitude": 40.7128, "longitude": -74.0060, "base_port_charges": 44000.0, "congestion_level": "Moderate"},
    {"name": "Port of Houston", "code": "USHOU", "country": "United States", "country_code": "US", "latitude": 29.7604, "longitude": -95.3698, "base_port_charges": 35000.0, "congestion_level": "Moderate"},
    {"name": "Port of Savannah", "code": "USSAV", "country": "United States", "country_code": "US", "latitude": 32.0809, "longitude": -81.0912, "base_port_charges": 33000.0, "congestion_level": "Low"},
    {"name": "Port of Vancouver", "code": "CAVAN", "country": "Canada", "country_code": "CA", "latitude": 49.2827, "longitude": -123.1207, "base_port_charges": 36000.0, "congestion_level": "Moderate"},
    {"name": "Port of Santos", "code": "BRSSZ", "country": "Brazil", "country_code": "BR", "latitude": -23.9618, "longitude": -46.3322, "base_port_charges": 30000.0, "congestion_level": "High"},
    {"name": "Port of Colon (Panama)", "code": "PAONX", "country": "Panama", "country_code": "PA", "latitude": 9.3598, "longitude": -79.9015, "base_port_charges": 31000.0, "congestion_level": "Moderate"},
    {"name": "Port of Buenos Aires", "code": "ARBUE", "country": "Argentina", "country_code": "AR", "latitude": -34.6037, "longitude": -58.3816, "base_port_charges": 29000.0, "congestion_level": "Low"},
    {"name": "Port of Durban", "code": "ZADUR", "country": "South Africa", "country_code": "ZA", "latitude": -29.8587, "longitude": 31.0218, "base_port_charges": 26000.0, "congestion_level": "High"},
    {"name": "Port of Cape Town", "code": "ZACPT", "country": "South Africa", "country_code": "ZA", "latitude": -33.9249, "longitude": 18.4241, "base_port_charges": 25000.0, "congestion_level": "Low"},
    {"name": "Port of Tangier Med", "code": "MATNG", "country": "Morocco", "country_code": "MA", "latitude": 35.8872, "longitude": -5.5033, "base_port_charges": 27000.0, "congestion_level": "Low"},
    {"name": "Port of Port Said", "code": "EGPSD", "country": "Egypt", "country_code": "EG", "latitude": 31.2653, "longitude": 32.3019, "base_port_charges": 32000.0, "congestion_level": "Moderate"}
]

VESSELS_SEED = [
    {"imo": "9812301", "mmsi": "211456789", "name": "Ocean Guardian", "ship_type": "Bulk Carrier - Panamax Class", "cargo_category": "Bulk", "dwt": 82000, "capacity_tons": 78000, "primary_fuel": "Bio-Methanol", "compatible_fuels": ["Bio-Methanol", "LNG", "VLSFO"], "service_speed": 14.5, "min_speed": 10.0, "max_speed": 17.5, "year_built": 2023, "flag_country": "Norway", "efficiency_rating": 0.88},
    {"imo": "9823412", "mmsi": "228567890", "name": "Nordic Pioneer", "ship_type": "Bulk Carrier - Capesize Class", "cargo_category": "Bulk", "dwt": 180000, "capacity_tons": 172000, "primary_fuel": "LNG", "compatible_fuels": ["LNG", "Bio-Methanol", "VLSFO"], "service_speed": 14.0, "min_speed": 9.5, "max_speed": 16.5, "year_built": 2024, "flag_country": "Liberia", "efficiency_rating": 0.85},
    {"imo": "9745123", "mmsi": "311678901", "name": "Pacific Harvest", "ship_type": "Bulk Carrier - Supramax Class", "cargo_category": "Bulk", "dwt": 58000, "capacity_tons": 55000, "primary_fuel": "VLSFO", "compatible_fuels": ["VLSFO", "Biofuel (B30)", "LSMGO"], "service_speed": 14.2, "min_speed": 10.0, "max_speed": 16.8, "year_built": 2019, "flag_country": "Panama", "efficiency_rating": 1.02},
    {"imo": "9856234", "mmsi": "352789012", "name": "Eco Voyager", "ship_type": "Bulk Carrier - Ultramax Class", "cargo_category": "Bulk", "dwt": 64000, "capacity_tons": 61000, "primary_fuel": "Bio-Methanol", "compatible_fuels": ["Bio-Methanol", "LNG", "Biofuel (B30)"], "service_speed": 14.8, "min_speed": 10.5, "max_speed": 17.2, "year_built": 2024, "flag_country": "Singapore", "efficiency_rating": 0.86},
    {"imo": "9689345", "mmsi": "477890123", "name": "Global Horizon", "ship_type": "Bulk Carrier - Handysize Class", "cargo_category": "Bulk", "dwt": 38000, "capacity_tons": 36000, "primary_fuel": "VLSFO", "compatible_fuels": ["VLSFO", "Biofuel (B30)"], "service_speed": 13.8, "min_speed": 9.5, "max_speed": 16.0, "year_built": 2017, "flag_country": "Marshall Islands", "efficiency_rating": 1.08},
    {"imo": "9890456", "mmsi": "563901234", "name": "Quantum Explorer", "ship_type": "Bulk Carrier - Post-Panamax Class", "cargo_category": "Bulk", "dwt": 95000, "capacity_tons": 90000, "primary_fuel": "Ammonia", "compatible_fuels": ["Ammonia", "LNG", "Bio-Methanol"], "service_speed": 15.0, "min_speed": 10.0, "max_speed": 18.0, "year_built": 2025, "flag_country": "Denmark", "efficiency_rating": 0.82},
    {"imo": "9911567", "mmsi": "219012345", "name": "Aurora Green", "ship_type": "Container - Ultra Large (24,000 TEU)", "cargo_category": "Container", "dwt": 220000, "capacity_tons": 210000, "primary_fuel": "Bio-Methanol", "compatible_fuels": ["Bio-Methanol", "LNG", "Biofuel (B30)"], "service_speed": 18.5, "min_speed": 12.0, "max_speed": 23.5, "year_built": 2024, "flag_country": "Denmark", "efficiency_rating": 0.84},
    {"imo": "9922678", "mmsi": "257123456", "name": "Eco Mariner", "ship_type": "Container - Neo-Panamax (15,000 TEU)", "cargo_category": "Container", "dwt": 155000, "capacity_tons": 145000, "primary_fuel": "LNG", "compatible_fuels": ["LNG", "Bio-Methanol", "VLSFO"], "service_speed": 18.0, "min_speed": 11.5, "max_speed": 22.5, "year_built": 2023, "flag_country": "France", "efficiency_rating": 0.86},
    {"imo": "9733789", "mmsi": "636234567", "name": "Atlantic Express", "ship_type": "Container - Post-Panamax (8,500 TEU)", "cargo_category": "Container", "dwt": 98000, "capacity_tons": 92000, "primary_fuel": "VLSFO", "compatible_fuels": ["VLSFO", "Biofuel (B30)", "LSMGO"], "service_speed": 19.0, "min_speed": 12.0, "max_speed": 24.0, "year_built": 2018, "flag_country": "Germany", "efficiency_rating": 1.05},
    {"imo": "9944890", "mmsi": "244345678", "name": "Zephyr Hydrogen", "ship_type": "Container - Feeder Max (3,500 TEU)", "cargo_category": "Container", "dwt": 45000, "capacity_tons": 42000, "primary_fuel": "Hydrogen", "compatible_fuels": ["Hydrogen", "Bio-Methanol", "LNG"], "service_speed": 16.5, "min_speed": 11.0, "max_speed": 20.0, "year_built": 2025, "flag_country": "Netherlands", "efficiency_rating": 0.79},
    {"imo": "9855901", "mmsi": "371456789", "name": "Solaris Wave", "ship_type": "Container - Panamax (5,000 TEU)", "cargo_category": "Container", "dwt": 65000, "capacity_tons": 60000, "primary_fuel": "LNG", "compatible_fuels": ["LNG", "Bio-Methanol", "Biofuel (B30)"], "service_speed": 17.5, "min_speed": 11.0, "max_speed": 21.5, "year_built": 2022, "flag_country": "Singapore", "efficiency_rating": 0.90},
    {"imo": "9666012", "mmsi": "538567890", "name": "Silver Wind", "ship_type": "Container - Regional Feeder (1,800 TEU)", "cargo_category": "Container", "dwt": 24000, "capacity_tons": 22000, "primary_fuel": "LSMGO", "compatible_fuels": ["LSMGO", "Biofuel (B30)", "VLSFO"], "service_speed": 16.0, "min_speed": 10.0, "max_speed": 19.5, "year_built": 2016, "flag_country": "Marshall Islands", "efficiency_rating": 1.12},
    {"imo": "9877123", "mmsi": "311789012", "name": "Neptune Titan", "ship_type": "Tanker - VLCC Class", "cargo_category": "Liquid", "dwt": 310000, "capacity_tons": 295000, "primary_fuel": "LNG", "compatible_fuels": ["LNG", "Bio-Methanol", "VLSFO"], "service_speed": 15.0, "min_speed": 10.0, "max_speed": 17.5, "year_built": 2023, "flag_country": "Greece", "efficiency_rating": 0.87},
    {"imo": "9888234", "mmsi": "229890123", "name": "Aegean Green", "ship_type": "Tanker - Suezmax Class", "cargo_category": "Liquid", "dwt": 158000, "capacity_tons": 150000, "primary_fuel": "Bio-Methanol", "compatible_fuels": ["Bio-Methanol", "LNG", "Biofuel (B30)"], "service_speed": 14.8, "min_speed": 10.0, "max_speed": 17.0, "year_built": 2024, "flag_country": "Malta", "efficiency_rating": 0.85},
    {"imo": "9799345", "mmsi": "636901234", "name": "Starlight Star", "ship_type": "Tanker - Aframax Class", "cargo_category": "Liquid", "dwt": 112000, "capacity_tons": 105000, "primary_fuel": "VLSFO", "compatible_fuels": ["VLSFO", "Biofuel (B30)", "LSMGO"], "service_speed": 14.5, "min_speed": 9.5, "max_speed": 16.8, "year_built": 2019, "flag_country": "Liberia", "efficiency_rating": 1.04},
    {"imo": "9900456", "mmsi": "354012345", "name": "Clean Hydro", "ship_type": "Tanker - MR2 Chemical Class", "cargo_category": "Liquid", "dwt": 50000, "capacity_tons": 47000, "primary_fuel": "Bio-Methanol", "compatible_fuels": ["Bio-Methanol", "Hydrogen", "LNG"], "service_speed": 14.2, "min_speed": 9.5, "max_speed": 16.5, "year_built": 2024, "flag_country": "Panama", "efficiency_rating": 0.84},
    {"imo": "9811567", "mmsi": "259123456", "name": "Polar Crystal", "ship_type": "Reefer - Arctic Pioneer", "cargo_category": "Refrigerated", "dwt": 22000, "capacity_tons": 19500, "primary_fuel": "LNG", "compatible_fuels": ["LNG", "Bio-Methanol", "Biofuel (B30)"], "service_speed": 18.0, "min_speed": 12.0, "max_speed": 22.0, "year_built": 2023, "flag_country": "Norway", "efficiency_rating": 0.88},
    {"imo": "9722678", "mmsi": "211234567", "name": "Baltic Frost", "ship_type": "Reefer - Nordic Carrier", "cargo_category": "Refrigerated", "dwt": 16000, "capacity_tons": 14000, "primary_fuel": "LSMGO", "compatible_fuels": ["LSMGO", "Biofuel (B30)", "VLSFO"], "service_speed": 17.5, "min_speed": 11.5, "max_speed": 21.0, "year_built": 2018, "flag_country": "Germany", "efficiency_rating": 1.06},
    {"imo": "9833789", "mmsi": "311345678", "name": "Terra Nova", "ship_type": "General Cargo - Multi-Purpose Heavy Lift", "cargo_category": "General", "dwt": 35000, "capacity_tons": 32000, "primary_fuel": "Bio-Methanol", "compatible_fuels": ["Bio-Methanol", "LNG", "Biofuel (B30)"], "service_speed": 15.2, "min_speed": 10.0, "max_speed": 18.0, "year_built": 2022, "flag_country": "Netherlands", "efficiency_rating": 0.90},
    {"imo": "9644890", "mmsi": "477456789", "name": "Pacific Trader", "ship_type": "General Cargo - Standard Box-Hold", "cargo_category": "General", "dwt": 28000, "capacity_tons": 26000, "primary_fuel": "VLSFO", "compatible_fuels": ["VLSFO", "Biofuel (B30)", "LSMGO"], "service_speed": 14.0, "min_speed": 9.5, "max_speed": 16.5, "year_built": 2017, "flag_country": "Hong Kong", "efficiency_rating": 1.09},
    {"imo": "9955901", "mmsi": "219567890", "name": "Quantum Horizon", "ship_type": "General Cargo - Green Multi-Carrier", "cargo_category": "General", "dwt": 42000, "capacity_tons": 39000, "primary_fuel": "Ammonia", "compatible_fuels": ["Ammonia", "Bio-Methanol", "LNG"], "service_speed": 15.5, "min_speed": 10.5, "max_speed": 18.5, "year_built": 2025, "flag_country": "Denmark", "efficiency_rating": 0.81}
]

EMISSION_FACTORS_SEED = [
    {"fuel_type": "VLSFO", "co2_factor": 3.114, "nox_factor": 78.0, "sox_factor": 10.0, "carbon_tax_rate": 85.0},
    {"fuel_type": "LSMGO", "co2_factor": 3.206, "nox_factor": 75.0, "sox_factor": 2.0, "carbon_tax_rate": 85.0},
    {"fuel_type": "LNG", "co2_factor": 2.750, "nox_factor": 15.0, "sox_factor": 0.05, "carbon_tax_rate": 85.0},
    {"fuel_type": "Bio-Methanol", "co2_factor": 0.450, "nox_factor": 20.0, "sox_factor": 0.0, "carbon_tax_rate": 85.0},
    {"fuel_type": "Biofuel (B30)", "co2_factor": 2.180, "nox_factor": 72.0, "sox_factor": 6.0, "carbon_tax_rate": 85.0},
    {"fuel_type": "Ammonia", "co2_factor": 0.050, "nox_factor": 22.0, "sox_factor": 0.0, "carbon_tax_rate": 85.0},
    {"fuel_type": "Hydrogen", "co2_factor": 0.000, "nox_factor": 5.0, "sox_factor": 0.0, "carbon_tax_rate": 85.0}
]

FUEL_PRICES_SEED = [
    {"fuel_type": "VLSFO", "price_per_ton": 615.0},
    {"fuel_type": "LSMGO", "price_per_ton": 790.0},
    {"fuel_type": "LNG", "price_per_ton": 540.0},
    {"fuel_type": "Bio-Methanol", "price_per_ton": 510.0},
    {"fuel_type": "Biofuel (B30)", "price_per_ton": 780.0},
    {"fuel_type": "Ammonia", "price_per_ton": 740.0},
    {"fuel_type": "Hydrogen", "price_per_ton": 1850.0}
]

def seed_database(db: Session):
    if db.query(Port).count() == 0:
        for p in PORTS_SEED:
            port_obj = Port(
                name=p["name"],
                code=p["code"],
                country=p["country"],
                country_code=p["country_code"],
                latitude=p["latitude"],
                longitude=p["longitude"],
                base_port_charges=p["base_port_charges"],
                congestion_level=p["congestion_level"],
                bunkering_fuels=["VLSFO", "LSMGO", "LNG", "Bio-Methanol"]
            )
            db.add(port_obj)
        db.commit()

    if db.query(Vessel).count() == 0:
        for v in VESSELS_SEED:
            vessel_obj = Vessel(
                imo_number=v["imo"],
                mmsi=v["mmsi"],
                name=v["name"],
                ship_type=v["ship_type"],
                cargo_category=v["cargo_category"],
                dwt=v["dwt"],
                capacity_tons=v["capacity_tons"],
                primary_fuel=v["primary_fuel"],
                compatible_fuels=v["compatible_fuels"],
                service_speed=v["service_speed"],
                min_speed=v["min_speed"],
                max_speed=v["max_speed"],
                year_built=v["year_built"],
                flag_country=v["flag_country"],
                efficiency_rating=v["efficiency_rating"]
            )
            db.add(vessel_obj)
        db.commit()

    if db.query(EmissionFactor).count() == 0:
        for ef in EMISSION_FACTORS_SEED:
            ef_obj = EmissionFactor(
                fuel_type=ef["fuel_type"],
                co2_factor=ef["co2_factor"],
                nox_factor=ef["nox_factor"],
                sox_factor=ef["sox_factor"],
                carbon_tax_rate=ef["carbon_tax_rate"]
            )
            db.add(ef_obj)
        db.commit()

    if db.query(FuelPrice).count() == 0:
        for fp in FUEL_PRICES_SEED:
            fp_obj = FuelPrice(
                fuel_type=fp["fuel_type"],
                price_per_ton=fp["price_per_ton"]
            )
            db.add(fp_obj)
        db.commit()

    demo_email = "operator@quantumfleet.com"
    if not db.query(User).filter(User.email == demo_email).first():
        demo_user = User(
            full_name="Aadesh Sharma",
            company_name="Oceanic Maritime Global",
            email=demo_email,
            hashed_password=get_password_hash("quantum2026"),
            role="Port Operator",
            is_active=True
        )
        db.add(demo_user)
        db.commit()
