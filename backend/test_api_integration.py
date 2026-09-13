from fastapi.testclient import TestClient
from app.main import app

def test_full_api_flow():
    client = TestClient(app)
    
    print("1. Health Check Endpoint")
    r = client.get("/api/health")
    assert r.status_code == 200, f"Health check failed: {r.text}"
    print("-> Health check OK:", r.json()["status"])
    
    print("\n2. Port Search / Autocomplete")
    r = client.get("/api/ports?search=singapore")
    assert r.status_code == 200
    ports = r.json()
    assert len(ports) >= 1
    print(f"-> Found {len(ports)} ports for 'singapore': {ports[0]['name']} ({ports[0]['code']})")
    
    print("\n3. Vessels List Endpoint (/api/vessels)")
    r = client.get("/api/vessels?category=Container")
    assert r.status_code == 200
    vessels = r.json()
    assert len(vessels) >= 5
    print(f"-> Found {len(vessels)} Container vessels in master database (e.g. {vessels[0]['name']})")
    
    print("\n4. ML Fuel Prediction (/api/predict-fuel)")
    ml_req = {
        "distance_nm": 8280.0,
        "cargo_weight_tons": 55000.0,
        "speed_knots": 16.5,
        "wind_speed_knots": 15.0,
        "wave_height_m": 2.1,
        "visibility_nm": 10.0,
        "fuel_type": "Bio-Methanol",
        "ship_type": "Container - Panamax (5,000 TEU)",
        "dwt": 65000.0
    }
    r = client.post("/api/predict-fuel", json=ml_req)
    assert r.status_code == 200, f"ML Predict failed: {r.text}"
    ml_res = r.json()
    print(f"-> Predicted Fuel Consumption: {ml_res['predicted_fuel_consumed_tons']} tons ({ml_res['model_used']})")
    print(f"-> Models comparison: {ml_res['all_models_comparison']}")
    
    print("\n5. Emission Calculation (/api/calculate-emission)")
    em_req = {"fuel_consumed_tons": 2500.0, "fuel_type": "Bio-Methanol"}
    r = client.post("/api/calculate-emission", json=em_req)
    assert r.status_code == 200
    em_res = r.json()
    print(f"-> CO2 Emissions: {em_res['co2_emissions_tons']} tons | Carbon Tax: ${em_res['carbon_tax_total_usd']:,.2f}")
    
    print("\n6. Carbon Tax Calculation (/api/calculate-tax)")
    tax_req = {"co2_emissions_tons": 1125.0, "fuel_cost_usd": 1275000.0, "port_charges_usd": 64000.0}
    r = client.post("/api/calculate-tax", json=tax_req)
    assert r.status_code == 200
    tax_res = r.json()
    print(f"-> Total Voyage Cost: ${tax_res['total_voyage_cost_usd']:,.2f} (Carbon Tax share: {tax_res['carbon_tax_share_pct']}%)")
    
    print("\n7. Executive Dashboard KPIs (/api/get-dashboard)")
    r = client.get("/api/get-dashboard")
    assert r.status_code == 200
    dash_res = r.json()
    print(f"-> Total Fleet Vessels: {dash_res['total_fleet_vessels']} | Utilization: {dash_res['average_fleet_utilization_pct']}%")
    
    print("\n8. AI Operational Insights (/api/ai-insights)")
    r = client.get("/api/ai-insights")
    assert r.status_code == 200
    insights = r.json()
    print(f"-> Generated {len(insights)} AI operational recommendations: '{insights[0]['title']}'")
    
    print("\n9. Optimizer Benchmark Suite (/api/benchmark-optimizers)")
    r = client.get("/api/benchmark-optimizers")
    assert r.status_code == 200
    benchmarks = r.json()["benchmarks"]
    for b in benchmarks:
        print(f"   • {b['algorithm']}: Time={b['execution_time_ms']}ms | Score={b['best_fitness_score']} | Cost Savings={b['cost_savings_pct']}% | CO2 Reduction={b['emission_reduction_pct']}%")
        
    print("\n10. User Login & Recommend Endpoint (/api/recommend)")
    login_payload = {"email": "operator@quantumfleet.com", "password": "quantum2026", "remember_me": True}
    r = client.post("/api/auth/login", json=login_payload)
    assert r.status_code == 200
    token = r.json()["access_token"]
    
    rec_req = {
        "from_port": "Port of Singapore",
        "to_port": "Port of Rotterdam",
        "cargo_weight": 48000,
        "cargo_type": "Container",
        "priority": "Balanced"
    }
    r = client.post("/api/recommend", json=rec_req, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    rec_res = r.json()
    print(f"-> Recommended Top 1: {rec_res['results'][0]['ship_type']} ({rec_res['results'][0]['fuel_type']}) - Cost: {rec_res['results'][0]['total_cost']} - Badge: {rec_res['results'][0]['emissions_badge']}")
    
    print("\n>>> ALL 10 MASTER API ENDPOINTS VERIFIED WITH 100% SUCCESS! <<<")

if __name__ == "__main__":
    test_full_api_flow()
