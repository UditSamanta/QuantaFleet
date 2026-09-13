-- ============================================================================
-- SIH26138 - QuantumFleet: Maritime Logistics & Green Fleet Database Schema
-- Database: PostgreSQL 14+
-- ============================================================================

-- Drop existing tables if re-initializing
DROP TABLE IF EXISTS optimization_results CASCADE;
DROP TABLE IF EXISTS emissions CASCADE;
DROP TABLE IF EXISTS voyages CASCADE;
DROP TABLE IF EXISTS weather CASCADE;
DROP TABLE IF EXISTS fuel_prices CASCADE;
DROP TABLE IF EXISTS vessels CASCADE;
DROP TABLE IF EXISTS ports CASCADE;
DROP TABLE IF EXISTS emission_factors CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 1. USERS TABLE (Authentication & Role Management)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(100) DEFAULT 'Port Operator', -- 'Fleet Manager', 'Port Operator', 'Logistics Admin'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- 2. PORTS TABLE (World Port Index Master Data)
CREATE TABLE ports (
    port_id SERIAL PRIMARY KEY,
    port_name VARCHAR(255) UNIQUE NOT NULL,
    code VARCHAR(10) UNIQUE,
    country VARCHAR(100) NOT NULL,
    country_code VARCHAR(5),
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    port_charges NUMERIC(12, 2) NOT NULL DEFAULT 25000.00,
    congestion_level VARCHAR(20) DEFAULT 'Moderate', -- 'Low', 'Moderate', 'High'
    bunkering_fuels JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ports_name ON ports(port_name);
CREATE INDEX idx_ports_country ON ports(country);

-- 3. VESSELS TABLE (Equasis Master Vessel Dataset)
CREATE TABLE vessels (
    vessel_id SERIAL PRIMARY KEY,
    imo_number VARCHAR(20) UNIQUE NOT NULL,
    mmsi VARCHAR(20) UNIQUE NOT NULL,
    ship_name VARCHAR(255) NOT NULL,
    ship_type VARCHAR(100) NOT NULL,
    cargo_category VARCHAR(50) NOT NULL DEFAULT 'General', -- 'Bulk', 'Container', 'Liquid', 'General', 'Refrigerated'
    dwt DOUBLE PRECISION NOT NULL,
    capacity DOUBLE PRECISION NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    compatible_fuels JSONB,
    service_speed DOUBLE PRECISION NOT NULL,
    min_speed DOUBLE PRECISION DEFAULT 10.0,
    max_speed DOUBLE PRECISION DEFAULT 24.0,
    year_built INTEGER NOT NULL,
    flag_country VARCHAR(100) NOT NULL,
    efficiency_rating DOUBLE PRECISION DEFAULT 1.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_vessels_imo ON vessels(imo_number);
CREATE INDEX idx_vessels_type ON vessels(ship_type);
CREATE INDEX idx_vessels_fuel ON vessels(fuel_type);

-- 4. EMISSION FACTORS TABLE (IMO Environmental Benchmark)
CREATE TABLE emission_factors (
    id SERIAL PRIMARY KEY,
    fuel_type VARCHAR(50) UNIQUE NOT NULL,
    co2_factor DOUBLE PRECISION NOT NULL, -- ton CO2 per ton fuel
    nox_factor DOUBLE PRECISION NOT NULL, -- kg NOx per ton fuel
    sox_factor DOUBLE PRECISION NOT NULL, -- kg SOx per ton fuel
    carbon_tax_rate DOUBLE PRECISION DEFAULT 85.00, -- USD per ton CO2 (EU ETS)
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. FUEL PRICES TABLE (Ship & Bunker Daily Quotes)
CREATE TABLE fuel_prices (
    id SERIAL PRIMARY KEY,
    quote_date DATE NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    price_per_ton NUMERIC(10, 2) NOT NULL,
    port_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_fuel_prices_lookup ON fuel_prices(fuel_type, quote_date);

-- 6. WEATHER DATASET (OpenWeather / Open-Meteo Marine Forecast)
CREATE TABLE weather (
    id SERIAL PRIMARY KEY,
    observation_date DATE NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    wind_speed DOUBLE PRECISION NOT NULL, -- in knots
    wave_height DOUBLE PRECISION NOT NULL, -- in meters
    temperature DOUBLE PRECISION NOT NULL, -- in Celsius
    visibility DOUBLE PRECISION NOT NULL, -- in nautical miles
    pressure DOUBLE PRECISION NOT NULL, -- in hPa
    ocean_current DOUBLE PRECISION NOT NULL, -- in knots
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_weather_coords ON weather(latitude, longitude, observation_date);

-- 7. VOYAGES TABLE (Kaggle / Datalastic Voyage Log)
CREATE TABLE voyages (
    voyage_id VARCHAR(50) PRIMARY KEY,
    vessel_imo VARCHAR(20) REFERENCES vessels(imo_number) ON DELETE CASCADE,
    departure_port VARCHAR(255) NOT NULL,
    arrival_port VARCHAR(255) NOT NULL,
    distance_nm DOUBLE PRECISION NOT NULL,
    travel_time_hours DOUBLE PRECISION NOT NULL,
    average_speed DOUBLE PRECISION NOT NULL,
    cargo_weight DOUBLE PRECISION NOT NULL,
    fuel_consumed DOUBLE PRECISION NOT NULL,
    arrival_delay DOUBLE PRECISION DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_voyages_ports ON voyages(departure_port, arrival_port);
CREATE INDEX idx_voyages_imo ON voyages(vessel_imo);

-- 8. EMISSIONS TABLE (EU MRV Verified Emissions Log)
CREATE TABLE emissions (
    id SERIAL PRIMARY KEY,
    vessel_imo VARCHAR(20) REFERENCES vessels(imo_number) ON DELETE CASCADE,
    voyage_id VARCHAR(50) REFERENCES voyages(voyage_id) ON DELETE SET NULL,
    fuel_type VARCHAR(50) NOT NULL,
    fuel_consumed_tons DOUBLE PRECISION NOT NULL,
    co2_emissions_tons DOUBLE PRECISION NOT NULL,
    nox_emissions_kg DOUBLE PRECISION,
    sox_emissions_kg DOUBLE PRECISION,
    carbon_tax_cost NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 9. OPTIMIZATION RESULTS TABLE (QPSO Results Cache & Telemetry)
CREATE TABLE optimization_results (
    id SERIAL PRIMARY KEY,
    query_hash VARCHAR(64) UNIQUE NOT NULL,
    origin_port VARCHAR(255) NOT NULL,
    destination_port VARCHAR(255) NOT NULL,
    cargo_weight DOUBLE PRECISION NOT NULL,
    cargo_type VARCHAR(50) NOT NULL,
    priority VARCHAR(50) NOT NULL,
    best_vessel_imo VARCHAR(20),
    best_fuel_type VARCHAR(50),
    best_speed_knots DOUBLE PRECISION,
    expected_savings_usd NUMERIC(12, 2),
    emission_reduction_pct DOUBLE PRECISION,
    ranked_solutions JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_optimization_hash ON optimization_results(query_hash);

-- ============================================================================
-- VIEWS & ANALYTICS
-- ============================================================================

-- View: Fleet Green Efficiency Summary
CREATE OR REPLACE VIEW view_fleet_green_summary AS
SELECT 
    v.ship_type,
    v.fuel_type,
    COUNT(v.vessel_id) AS total_vessels,
    AVG(v.dwt) AS avg_dwt,
    AVG(v.service_speed) AS avg_speed,
    ef.co2_factor,
    ef.carbon_tax_rate
FROM vessels v
LEFT JOIN emission_factors ef ON v.fuel_type = ef.fuel_type
GROUP BY v.ship_type, v.fuel_type, ef.co2_factor, ef.carbon_tax_rate;

-- ============================================================================
-- SAMPLE DATA INSERTION COMMENTARY
-- ============================================================================
-- Data ingestion is managed via the python ETL script: backend/data_pipeline/etl_pipeline.py
