import os
import csv
import random
import datetime
import math
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "datasets")
os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)
np.random.seed(42)

def haversine_distance_nm(lat1, lon1, lat2, lon2):
    R_km = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlambda = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dphi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return (R_km * c) / 1.852

# 1. Ports Dataset (ports.csv)
PORTS_DATA = [
    (1, "Port of Singapore", "Singapore", 1.290270, 103.851959, 32000.0, "Moderate"),
    (2, "Port of Shanghai", "China", 31.230416, 121.473701, 38000.0, "High"),
    (3, "Port of Ningbo-Zhoushan", "China", 29.8683, 121.5440, 34000.0, "Moderate"),
    (4, "Port of Shenzhen", "China", 22.5431, 114.0579, 33000.0, "Moderate"),
    (5, "Port of Busan", "South Korea", 35.1796, 129.0756, 28000.0, "Low"),
    (6, "Port of Hong Kong", "Hong Kong", 22.3193, 114.1694, 31000.0, "Moderate"),
    (7, "Port of Tokyo", "Japan", 35.6762, 139.6503, 35000.0, "Low"),
    (8, "Port of Yokohama", "Japan", 35.4437, 139.6380, 32000.0, "Low"),
    (9, "Port of Klang", "Malaysia", 3.0000, 101.4000, 24000.0, "Moderate"),
    (10, "Port of Tanjung Pelepas", "Malaysia", 1.3620, 103.5490, 23000.0, "Low"),
    (11, "Port of Kaohsiung", "Taiwan", 22.6273, 120.3014, 27000.0, "Low"),
    (12, "Port of Sydney", "Australia", -33.8688, 151.2093, 36000.0, "Low"),
    (13, "Port of Melbourne", "Australia", -37.8136, 144.9631, 34000.0, "Low"),
    (14, "Jawaharlal Nehru Port (JNPT)", "India", 18.9499, 72.9515, 22000.0, "Moderate"),
    (15, "Port of Chennai", "India", 13.0827, 80.2707, 20000.0, "Moderate"),
    (16, "Port of Mundra", "India", 22.8396, 69.7042, 21000.0, "Low"),
    (17, "Port of Colombo", "Sri Lanka", 6.9271, 79.8612, 25000.0, "Moderate"),
    (18, "Port of Jebel Ali (Dubai)", "United Arab Emirates", 25.0113, 55.0612, 30000.0, "Moderate"),
    (19, "Port of Salalah", "Oman", 16.9442, 54.0041, 23000.0, "Low"),
    (20, "King Abdullah Port", "Saudi Arabia", 22.5367, 39.0967, 26000.0, "Low"),
    (21, "Port of Rotterdam", "Netherlands", 51.9244, 4.4777, 39000.0, "Moderate"),
    (22, "Port of Antwerp-Bruges", "Belgium", 51.2194, 4.4025, 36000.0, "Moderate"),
    (23, "Port of Hamburg", "Germany", 53.5511, 9.9937, 37000.0, "Moderate"),
    (24, "Port of Valencia", "Spain", 39.4699, -0.3763, 29000.0, "Low"),
    (25, "Port of Algeciras", "Spain", 36.1408, -5.4562, 28000.0, "Low"),
    (26, "Port of Piraeus", "Greece", 37.9430, 23.6470, 27000.0, "Moderate"),
    (27, "Port of Felixstowe", "United Kingdom", 51.9634, 1.3511, 33000.0, "Moderate"),
    (28, "Port of Le Havre", "France", 49.4944, 0.1079, 31000.0, "Low"),
    (29, "Port of Genoa", "Italy", 44.4056, 8.9463, 30000.0, "Low"),
    (30, "Port of Los Angeles", "United States", 33.7432, -118.2673, 42000.0, "High"),
    (31, "Port of Long Beach", "United States", 33.7701, -118.1937, 41000.0, "Moderate"),
    (32, "Port of New York & New Jersey", "United States", 40.7128, -74.0060, 44000.0, "Moderate"),
    (33, "Port of Houston", "United States", 29.7604, -95.3698, 35000.0, "Moderate"),
    (34, "Port of Savannah", "United States", 32.0809, -81.0912, 33000.0, "Low"),
    (35, "Port of Vancouver", "Canada", 49.2827, -123.1207, 36000.0, "Moderate"),
    (36, "Port of Santos", "Brazil", -23.9618, -46.3322, 30000.0, "High"),
    (37, "Port of Colon (Panama)", "Panama", 9.3598, -79.9015, 31000.0, "Moderate"),
    (38, "Port of Buenos Aires", "Argentina", -34.6037, -58.3816, 29000.0, "Low"),
    (39, "Port of Durban", "South Africa", -29.8587, 31.0218, 26000.0, "High"),
    (40, "Port of Cape Town", "South Africa", -33.9249, 18.4241, 25000.0, "Low"),
    (41, "Port of Tangier Med", "Morocco", 35.8872, -5.5033, 27000.0, "Low"),
    (42, "Port of Port Said", "Egypt", 31.2653, 32.3019, 32000.0, "Moderate")
]

# 2. Emission Factors
EMISSION_FACTORS_DATA = [
    ("VLSFO", 3.114, 78.0, 10.0, 85.0),
    ("LSMGO", 3.206, 75.0, 2.0, 85.0),
    ("LNG", 2.750, 15.0, 0.05, 85.0),
    ("Bio-Methanol", 0.450, 20.0, 0.0, 85.0),
    ("Biofuel (B30)", 2.180, 72.0, 6.0, 85.0),
    ("Ammonia", 0.050, 22.0, 0.0, 85.0),
    ("Hydrogen", 0.000, 5.0, 0.0, 85.0)
]

# 3. Vessels List (105 Vessels)
VESSEL_TYPES = [
    ("Bulk Carrier - Capesize Class", "Bulk", (160000, 210000), 14.0),
    ("Bulk Carrier - Panamax Class", "Bulk", (70000, 85000), 14.5),
    ("Bulk Carrier - Supramax Class", "Bulk", (50000, 65000), 14.2),
    ("Bulk Carrier - Handysize Class", "Bulk", (25000, 40000), 13.8),
    ("Container - Ultra Large (24,000 TEU)", "Container", (200000, 240000), 18.5),
    ("Container - Neo-Panamax (15,000 TEU)", "Container", (130000, 165000), 18.0),
    ("Container - Post-Panamax (8,500 TEU)", "Container", (80000, 110000), 19.0),
    ("Container - Panamax (5,000 TEU)", "Container", (55000, 75000), 17.5),
    ("Container - Feeder Max (3,500 TEU)", "Container", (35000, 50000), 16.5),
    ("Container - Regional Feeder (1,800 TEU)", "Container", (18000, 28000), 16.0),
    ("Tanker - VLCC Class", "Liquid", (280000, 320000), 15.0),
    ("Tanker - Suezmax Class", "Liquid", (140000, 165000), 14.8),
    ("Tanker - Aframax Class", "Liquid", (95000, 120000), 14.5),
    ("Tanker - MR2 Chemical Class", "Liquid", (42000, 55000), 14.2),
    ("Reefer - Arctic Pioneer", "Refrigerated", (18000, 25000), 18.0),
    ("Reefer - Nordic Carrier", "Refrigerated", (12000, 18000), 17.5),
    ("General Cargo - Multi-Purpose Heavy Lift", "General", (28000, 40000), 15.2),
    ("General Cargo - Standard Box-Hold", "General", (20000, 30000), 14.0),
    ("General Cargo - Green Multi-Carrier", "General", (35000, 48000), 15.5)
]

FLAGS = ["Panama", "Liberia", "Marshall Islands", "Singapore", "Hong Kong", "Norway", "Denmark", "Greece", "Germany", "Malta", "Netherlands"]
FUELS = ["VLSFO", "LSMGO", "LNG", "Bio-Methanol", "Biofuel (B30)", "Ammonia", "Hydrogen"]

LHV_MAP = {
    "VLSFO": 1.0, "LSMGO": 0.98, "LNG": 0.85, "Bio-Methanol": 2.15,
    "Biofuel (B30)": 1.05, "Ammonia": 2.30, "Hydrogen": 0.35
}

CO2_FACTOR_MAP = {
    "VLSFO": 3.114, "LSMGO": 3.206, "LNG": 2.750, "Bio-Methanol": 0.450,
    "Biofuel (B30)": 2.180, "Ammonia": 0.050, "Hydrogen": 0.000
}

def generate_all():
    print("=== Generating 7 Standard SIH Maritime Datasets ===")
    
    # 1. Ports
    ports_path = os.path.join(OUTPUT_DIR, "ports.csv")
    with open(ports_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Port_ID", "Port_Name", "Country", "Latitude", "Longitude", "Port_Charges", "Congestion_Level"])
        for p in PORTS_DATA:
            w.writerow(p)
    print(f"[OK] {len(PORTS_DATA)} records written to {ports_path}")
    
    # 2. Emission Factors
    ef_path = os.path.join(OUTPUT_DIR, "emission_factors.csv")
    with open(ef_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Fuel_Type", "CO2_Factor", "NOx_Factor", "SOx_Factor", "Carbon_Tax_Rate"])
        for ef in EMISSION_FACTORS_DATA:
            w.writerow(ef)
    print(f"[OK] {len(EMISSION_FACTORS_DATA)} records written to {ef_path}")
    
    # 3. Fuel Prices
    fp_path = os.path.join(OUTPUT_DIR, "fuel_prices.csv")
    base_prices = {"VLSFO": 615.0, "LSMGO": 790.0, "LNG": 540.0, "Bio-Methanol": 510.0, "Biofuel (B30)": 780.0, "Ammonia": 740.0, "Hydrogen": 1850.0}
    dates = [(datetime.date(2026, 8, 1) + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(35)]
    fp_rows = []
    for d in dates:
        for port_row in PORTS_DATA[:10]:
            for ftype, bp in base_prices.items():
                price = round(max(300.0, bp + random.uniform(-15.0, 15.0)), 2)
                fp_rows.append([d, ftype, price, port_row[1]])
    with open(fp_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Date", "Fuel_Type", "Price_Per_Ton", "Port"])
        for r in fp_rows:
            w.writerow(r)
    print(f"[OK] {len(fp_rows)} records written to {fp_path}")
    
    # 4. Vessels (105 Vessels)
    vessels_path = os.path.join(OUTPUT_DIR, "vessels.csv")
    vessels = []
    ship_prefixes = ["Ocean", "Nordic", "Pacific", "Eco", "Global", "Quantum", "Aurora", "Atlantic", "Zephyr", "Solaris", "Silver", "Neptune", "Aegean", "Starlight", "Clean", "Polar", "Baltic", "Terra", "Apex", "Horizon", "Emerald", "Vanguard", "Poseidon", "Titan"]
    ship_suffixes = ["Leader", "Guardian", "Pioneer", "Harvest", "Voyager", "Horizon", "Explorer", "Green", "Mariner", "Express", "Wave", "Wind", "Titan", "Star", "Hydro", "Crystal", "Frost", "Nova", "Trader", "Pride", "Navigator"]
    
    imo_start = 9800001
    for i in range(105):
        imo = str(imo_start + i)
        mmsi = str(200000000 + random.randint(10000000, 99999999))
        name = f"{random.choice(ship_prefixes)} {random.choice(ship_suffixes)} {random.randint(1, 99)}"
        stype, category, (dwt_min, dwt_max), s_speed = VESSEL_TYPES[i % len(VESSEL_TYPES)]
        dwt = round(random.uniform(dwt_min, dwt_max), -2)
        capacity = round(dwt * random.uniform(0.90, 0.96), -2)
        primary_fuel = random.choice(FUELS)
        speed = round(s_speed + random.uniform(-0.5, 0.5), 1)
        year_built = random.randint(2015, 2025)
        flag = random.choice(FLAGS)
        
        vessels.append({
            "IMO_Number": imo, "MMSI": mmsi, "Ship_Name": name, "Ship_Type": stype,
            "Category": category, "DWT": dwt, "Capacity": capacity,
            "Fuel_Type": primary_fuel, "Service_Speed": speed, "Year_Built": year_built,
            "Flag_Country": flag
        })
    with open(vessels_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["IMO_Number", "MMSI", "Ship_Name", "Ship_Type", "DWT", "Capacity", "Fuel_Type", "Service_Speed", "Year_Built", "Flag_Country"])
        for v in vessels:
            w.writerow([v["IMO_Number"], v["MMSI"], v["Ship_Name"], v["Ship_Type"], v["DWT"], v["Capacity"], v["Fuel_Type"], v["Service_Speed"], v["Year_Built"], v["Flag_Country"]])
    print(f"[OK] {len(vessels)} vessels written to {vessels_path}")
    
    # 5. Weather
    weather_path = os.path.join(OUTPUT_DIR, "weather.csv")
    w_rows = []
    start_date = datetime.date(2026, 1, 1)
    for i in range(120):
        cdate = (start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        for p in PORTS_DATA[:15]:
            lat = p[3] + random.uniform(-3.0, 3.0)
            lon = p[4] + random.uniform(-3.0, 3.0)
            abs_lat = abs(lat)
            wind_speed = round(random.uniform(8.0, 25.0) + (abs_lat / 90.0) * 12.0, 1)
            wave_height = round(random.uniform(0.8, 2.5) + (abs_lat / 90.0) * 2.0, 2)
            temp = round(28.0 - (abs_lat / 90.0) * 35.0 + random.uniform(-2, 2), 1)
            visibility = round(random.uniform(7.0, 15.0), 1)
            pressure = round(random.uniform(995.0, 1025.0), 1)
            current = round(random.uniform(0.2, 2.4), 2)
            w_rows.append([cdate, round(lat, 4), round(lon, 4), wind_speed, wave_height, temp, visibility, pressure, current])
    with open(weather_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Date", "Latitude", "Longitude", "Wind_Speed", "Wave_Height", "Temperature", "Visibility", "Pressure", "Ocean_Current"])
        for r in w_rows:
            w.writerow(r)
    print(f"[OK] {len(w_rows)} weather records written to {weather_path}")
    
    # 6. Voyages (voyages.csv) & 7. Fuel Consumption (fuel_consumption.csv)
    voyages_path = os.path.join(OUTPUT_DIR, "voyages.csv")
    fuel_path = os.path.join(OUTPUT_DIR, "fuel_consumption.csv")
    
    voyage_rows = []
    fuel_rows = []
    vid_counter = 10001
    
    for v in vessels:
        n_voyages = random.randint(10, 15)
        for _ in range(n_voyages):
            vid = f"VOY-{vid_counter}"
            vid_counter += 1
            p1, p2 = random.sample(PORTS_DATA, 2)
            dist = round(haversine_distance_nm(p1[3], p1[4], p2[3], p2[4]) * 1.25, 1)
            speed = round(v["Service_Speed"] * random.uniform(0.88, 1.05), 1)
            travel_hours = round(dist / speed, 1)
            cargo_wt = round(v["Capacity"] * random.uniform(0.65, 0.98), -2)
            fuel_type = v["Fuel_Type"]
            
            # Hydrodynamic Admiralty Model
            disp = v["DWT"] * (0.25 + (cargo_wt / v["DWT"]))
            power_kw = (math.pow(disp, 2.0/3.0) * math.pow(speed, 3.1)) / 550.0
            weather_mult = random.uniform(1.02, 1.15)
            lhv_mult = LHV_MAP.get(fuel_type, 1.0)
            fuel_cons = round((power_kw * 172.0 * travel_hours / 1e6) * weather_mult * lhv_mult, 2)
            delay = round(random.choice([0.0, 0.0, 0.0, 1.5, 3.0, 6.5, 12.0, 24.0]), 1)
            
            voyage_rows.append([vid, v["IMO_Number"], p1[1], p2[1], dist, travel_hours, speed, cargo_wt, fuel_cons, delay])
            co2_tons = round(fuel_cons * CO2_FACTOR_MAP.get(fuel_type, 3.114), 2)
            fuel_rows.append([v["IMO_Number"], v["Ship_Type"], dist, fuel_cons, fuel_type, co2_tons])
            
    with open(voyages_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Voyage_ID", "Vessel_IMO", "Departure_Port", "Arrival_Port", "Distance_NM", "Travel_Time_Hours", "Average_Speed", "Cargo_Weight", "Fuel_Consumed", "Arrival_Delay"])
        for r in voyage_rows:
            w.writerow(r)
            
    with open(fuel_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Vessel_IMO", "Ship_Type", "Distance", "Fuel_Consumed", "Fuel_Type", "CO2_Emissions"])
        for r in fuel_rows:
            w.writerow(r)
            
    print(f"[OK] {len(voyage_rows)} voyages written to {voyages_path}")
    print(f"[OK] {len(fuel_rows)} EU MRV fuel consumption records written to {fuel_path}")
    print("=== All 7 Datasets Generated Successfully in /datasets ===")

if __name__ == "__main__":
    generate_all()
