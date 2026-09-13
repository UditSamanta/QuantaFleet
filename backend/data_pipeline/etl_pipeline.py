import os
import csv
import json
from sqlalchemy.orm import Session
from ..app.database import engine, Base, SessionLocal
from ..app.models.maritime import Vessel, Port, Voyage, EmissionFactor, FuelPrice
from ..app.models.user import User
from ..app.auth.security import get_password_hash

DATASETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "datasets")

# Canonical Port UN/LOCODEs
PORT_CODES = {
    "Port of Singapore": ("SGSIN", "SG"),
    "Port of Shanghai": ("CNSHA", "CN"),
    "Port of Ningbo-Zhoushan": ("CNNGB", "CN"),
    "Port of Shenzhen": ("CNSZX", "CN"),
    "Port of Busan": ("KRPUS", "KR"),
    "Port of Hong Kong": ("HKHKG", "HK"),
    "Port of Tokyo": ("JPTYO", "JP"),
    "Port of Yokohama": ("JPYOK", "JP"),
    "Port of Klang": ("MYPKG", "MY"),
    "Port of Tanjung Pelepas": ("MYTPP", "MY"),
    "Port of Kaohsiung": ("TWKHH", "TW"),
    "Port of Sydney": ("AUSYD", "AU"),
    "Port of Melbourne": ("AUMEL", "AU"),
    "Jawaharlal Nehru Port (JNPT)": ("INNSA", "IN"),
    "Port of Chennai": ("INMAA", "IN"),
    "Port of Mundra": ("INMUN", "IN"),
    "Port of Colombo": ("LKCMB", "LK"),
    "Port of Jebel Ali (Dubai)": ("AEJEA", "AE"),
    "Port of Salalah": ("OMSLL", "OM"),
    "King Abdullah Port": ("SAKAP", "SA"),
    "Port of Rotterdam": ("NLRTM", "NL"),
    "Port of Antwerp-Bruges": ("BEANR", "BE"),
    "Port of Hamburg": ("DEHAM", "DE"),
    "Port of Valencia": ("ESVLC", "ES"),
    "Port of Algeciras": ("ESALG", "ES"),
    "Port of Piraeus": ("GRPIR", "GR"),
    "Port of Felixstowe": ("GBFXT", "GB"),
    "Port of Le Havre": ("FRLEH", "FR"),
    "Port of Genoa": ("ITGOA", "IT"),
    "Port of Los Angeles": ("USLAX", "US"),
    "Port of Long Beach": ("USLGB", "US"),
    "Port of New York & New Jersey": ("USNYC", "US"),
    "Port of Houston": ("USHOU", "US"),
    "Port of Savannah": ("USSAV", "US"),
    "Port of Vancouver": ("CAVAN", "CA"),
    "Port of Santos": ("BRSSZ", "BR"),
    "Port of Colon (Panama)": ("PAONX", "PA"),
    "Port of Buenos Aires": ("ARBUE", "AR"),
    "Port of Durban": ("ZADUR", "ZA"),
    "Port of Cape Town": ("ZACPT", "ZA"),
    "Port of Tangier Med": ("MATNG", "MA"),
    "Port of Port Said": ("EGPSD", "EG")
}

class MaritimeETLPipeline:
    def __init__(self, db: Session):
        self.db = db
        self.stats = {
            "ports_loaded": 0,
            "vessels_loaded": 0,
            "emission_factors_loaded": 0,
            "fuel_prices_loaded": 0,
            "voyages_loaded": 0,
            "validation_errors": 0
        }

    def run_etl(self):
        print(">>> Starting Maritime Data ETL Pipeline <<<")
        Base.metadata.create_all(bind=engine)
        
        self.load_ports()
        self.load_emission_factors()
        self.load_fuel_prices()
        self.load_vessels()
        self.load_voyages()
        self.seed_admin_user()
        
        print("\n>>> ETL Summary Statistics <<<")
        for k, v in self.stats.items():
            print(f"  • {k.replace('_', ' ').title()}: {v}")
        print(">>> ETL Pipeline Completed Successfully! <<<\n")

    def load_ports(self):
        path = os.path.join(DATASETS_DIR, "ports.csv")
        if not os.path.exists(path):
            return
            
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                pname = r["Port_Name"]
                existing = self.db.query(Port).filter(Port.name == pname).first()
                if not existing:
                    pcode, ccode = PORT_CODES.get(pname, (f"PRT{r['Port_ID']}", r["Country"][:2].upper()))
                    port_obj = Port(
                        name=pname,
                        code=pcode,
                        country=r["Country"],
                        country_code=ccode,
                        latitude=float(r["Latitude"]),
                        longitude=float(r["Longitude"]),
                        base_port_charges=float(r["Port_Charges"]),
                        congestion_level=r["Congestion_Level"],
                        bunkering_fuels=["VLSFO", "LSMGO", "LNG", "Bio-Methanol"]
                    )
                    self.db.add(port_obj)
                    self.stats["ports_loaded"] += 1
        self.db.commit()

    def load_emission_factors(self):
        path = os.path.join(DATASETS_DIR, "emission_factors.csv")
        if not os.path.exists(path):
            return
            
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                existing = self.db.query(EmissionFactor).filter(EmissionFactor.fuel_type == r["Fuel_Type"]).first()
                if not existing:
                    ef_obj = EmissionFactor(
                        fuel_type=r["Fuel_Type"],
                        co2_factor=float(r["CO2_Factor"]),
                        nox_factor=float(r["NOx_Factor"]),
                        sox_factor=float(r["SOx_Factor"]),
                        carbon_tax_rate=float(r["Carbon_Tax_Rate"])
                    )
                    self.db.add(ef_obj)
                    self.stats["emission_factors_loaded"] += 1
        self.db.commit()

    def load_fuel_prices(self):
        path = os.path.join(DATASETS_DIR, "fuel_prices.csv")
        if not os.path.exists(path):
            return
            
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            latest_prices = {}
            for r in reader:
                latest_prices[r["Fuel_Type"]] = float(r["Price_Per_Ton"])
                
            for ftype, price in latest_prices.items():
                existing = self.db.query(FuelPrice).filter(FuelPrice.fuel_type == ftype).first()
                if not existing:
                    fp_obj = FuelPrice(fuel_type=ftype, price_per_ton=price)
                    self.db.add(fp_obj)
                    self.stats["fuel_prices_loaded"] += 1
                else:
                    existing.price_per_ton = price
        self.db.commit()

    def load_vessels(self):
        path = os.path.join(DATASETS_DIR, "vessels.csv")
        if not os.path.exists(path):
            return
            
        fuel_compat = {
            "LNG": ["LNG", "Bio-Methanol", "VLSFO"],
            "Bio-Methanol": ["Bio-Methanol", "LNG", "Biofuel (B30)"],
            "Ammonia": ["Ammonia", "LNG", "Bio-Methanol"],
            "Hydrogen": ["Hydrogen", "Bio-Methanol", "LNG"],
            "VLSFO": ["VLSFO", "Biofuel (B30)", "LSMGO"],
            "LSMGO": ["LSMGO", "Biofuel (B30)", "VLSFO"],
            "Biofuel (B30)": ["Biofuel (B30)", "VLSFO", "LSMGO"]
        }
        
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                existing = self.db.query(Vessel).filter(Vessel.imo_number == r["IMO_Number"]).first()
                if not existing:
                    stype = r["Ship_Type"]
                    if "Bulk" in stype:
                        cat = "Bulk"
                    elif "Container" in stype:
                        cat = "Container"
                    elif "Tanker" in stype:
                        cat = "Liquid"
                    elif "Reefer" in stype:
                        cat = "Refrigerated"
                    else:
                        cat = "General"
                        
                    primary_f = r["Fuel_Type"]
                    v_obj = Vessel(
                        imo_number=r["IMO_Number"],
                        mmsi=r["MMSI"],
                        name=r["Ship_Name"],
                        ship_type=stype,
                        cargo_category=cat,
                        dwt=float(r["DWT"]),
                        capacity_tons=float(r["Capacity"]),
                        primary_fuel=primary_f,
                        compatible_fuels=fuel_compat.get(primary_f, [primary_f]),
                        service_speed=float(r["Service_Speed"]),
                        min_speed=10.0,
                        max_speed=24.0,
                        year_built=int(r["Year_Built"]),
                        flag_country=r["Flag_Country"],
                        efficiency_rating=round(1.0 - (int(r["Year_Built"]) - 2015) * 0.015, 2)
                    )
                    self.db.add(v_obj)
                    self.stats["vessels_loaded"] += 1
        self.db.commit()

    def load_voyages(self):
        path = os.path.join(DATASETS_DIR, "voyages.csv")
        if not os.path.exists(path):
            return
            
        port_cache = {p.name: p.id for p in self.db.query(Port).all()}
        vessel_cache = {v.imo_number: v.id for v in self.db.query(Vessel).all()}
        
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for r in reader:
                vid = r["Voyage_ID"]
                existing = self.db.query(Voyage).filter(Voyage.voyage_id == vid).first()
                if not existing:
                    dep_id = port_cache.get(r["Departure_Port"])
                    arr_id = port_cache.get(r["Arrival_Port"])
                    v_id = vessel_cache.get(r["Vessel_IMO"])
                    
                    if dep_id and arr_id and v_id:
                        voy_obj = Voyage(
                            voyage_id=vid,
                            departure_port_id=dep_id,
                            arrival_port_id=arr_id,
                            vessel_id=v_id,
                            distance_nm=float(r["Distance_NM"]),
                            travel_time_hours=float(r["Travel_Time_Hours"]),
                            avg_speed_knots=float(r["Average_Speed"]),
                            cargo_weight_tons=float(r["Cargo_Weight"]),
                            fuel_type="VLSFO",
                            fuel_consumed_tons=float(r["Fuel_Consumed"]),
                            weather_risk="Low"
                        )
                        self.db.add(voy_obj)
                        self.stats["voyages_loaded"] += 1
                        count += 1
                        if count % 200 == 0:
                            self.db.commit()
        self.db.commit()

    def seed_admin_user(self):
        demo_email = "operator@quantumfleet.com"
        if not self.db.query(User).filter(User.email == demo_email).first():
            demo_user = User(
                full_name="Aadesh Sharma",
                company_name="Oceanic Maritime Global",
                email=demo_email,
                hashed_password=get_password_hash("quantum2026"),
                role="Port Operator",
                is_active=True
            )
            self.db.add(demo_user)
            self.db.commit()

def main():
    db = SessionLocal()
    try:
        pipeline = MaritimeETLPipeline(db)
        pipeline.run_etl()
    finally:
        db.close()

if __name__ == "__main__":
    main()
