import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from ..database import Base

class Vessel(Base):
    __tablename__ = "vessels"

    id = Column(Integer, primary_key=True, index=True)
    imo_number = Column(String(20), unique=True, index=True, nullable=False)
    mmsi = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    ship_type = Column(String(100), nullable=False)
    cargo_category = Column(String(50), nullable=False)  # Bulk, Container, General, Liquid, Refrigerated
    dwt = Column(Float, nullable=False)  # Deadweight tonnage
    capacity_tons = Column(Float, nullable=False)
    primary_fuel = Column(String(50), nullable=False)
    compatible_fuels = Column(JSON, nullable=False)
    service_speed = Column(Float, nullable=False)  # Design speed in knots
    min_speed = Column(Float, default=10.0)
    max_speed = Column(Float, default=24.0)
    year_built = Column(Integer, nullable=False)
    flag_country = Column(String(100), nullable=False)
    efficiency_rating = Column(Float, default=1.0)

class Port(Base):
    __tablename__ = "ports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    code = Column(String(10), unique=True, index=True, nullable=False)
    country = Column(String(100), nullable=False)
    country_code = Column(String(5), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    base_port_charges = Column(Float, nullable=False)
    congestion_level = Column(String(20), default="Moderate")
    bunkering_fuels = Column(JSON, nullable=True)

class Voyage(Base):
    __tablename__ = "voyages"

    id = Column(Integer, primary_key=True, index=True)
    voyage_id = Column(String(50), unique=True, index=True, nullable=False)
    departure_port_id = Column(Integer, ForeignKey("ports.id"), nullable=False)
    arrival_port_id = Column(Integer, ForeignKey("ports.id"), nullable=False)
    vessel_id = Column(Integer, ForeignKey("vessels.id"), nullable=False)
    distance_nm = Column(Float, nullable=False)
    travel_time_hours = Column(Float, nullable=False)
    avg_speed_knots = Column(Float, nullable=False)
    cargo_weight_tons = Column(Float, nullable=False)
    fuel_type = Column(String(50), nullable=False)
    fuel_consumed_tons = Column(Float, nullable=False)
    weather_risk = Column(String(20), default="Low")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class EmissionFactor(Base):
    __tablename__ = "emission_factors"

    id = Column(Integer, primary_key=True, index=True)
    fuel_type = Column(String(50), unique=True, index=True, nullable=False)
    co2_factor = Column(Float, nullable=False)  # Ton CO2 per ton of fuel
    nox_factor = Column(Float, nullable=False)
    sox_factor = Column(Float, nullable=False)
    carbon_tax_rate = Column(Float, default=85.0)  # USD per ton CO2

class FuelPrice(Base):
    __tablename__ = "fuel_prices"

    id = Column(Integer, primary_key=True, index=True)
    fuel_type = Column(String(50), unique=True, index=True, nullable=False)
    price_per_ton = Column(Float, nullable=False)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

class OptimizationCache(Base):
    __tablename__ = "optimization_cache"

    id = Column(Integer, primary_key=True, index=True)
    cache_key = Column(String(255), unique=True, index=True, nullable=False)
    results = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
