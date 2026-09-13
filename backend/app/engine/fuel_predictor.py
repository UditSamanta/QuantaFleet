import numpy as np
import math
from sklearn.ensemble import GradientBoostingRegressor

class FuelPredictionModel:
    """
    Hybrid Machine Learning + Naval Architecture Fuel Consumption Predictor.
    Combines Admiralty hydrodynamic displacement-speed law with Gradient Boosting.
    """
    def __init__(self):
        self.model = None
        self._fuel_energy_densities = {
            "VLSFO": 1.0,
            "LSMGO": 0.98,
            "LNG": 0.85,
            "Bio-Methanol": 2.15,
            "Ammonia": 2.30,
            "Hydrogen": 0.35,
            "Biofuel (B30)": 1.05
        }
        self._train_initial_model()

    def _train_initial_model(self):
        np.random.seed(42)
        n_samples = 3000
        
        dwt_samples = np.random.uniform(10000, 220000, n_samples)
        cargo_ratio_samples = np.random.uniform(0.3, 0.98, n_samples)
        speed_samples = np.random.uniform(10.0, 22.0, n_samples)
        distance_samples = np.random.uniform(200, 12000, n_samples)
        weather_penalty_samples = np.random.uniform(1.0, 1.25, n_samples)
        fuel_lhv_samples = np.random.choice([1.0, 0.98, 0.85, 2.15, 2.30, 0.35, 1.05], n_samples)
        efficiency_rating_samples = np.random.uniform(0.82, 1.15, n_samples)
        
        displacement = dwt_samples * (0.25 + cargo_ratio_samples)
        power_kw = (np.power(displacement, 2.0/3.0) * np.power(speed_samples, 3.1)) / 550.0
        voyage_hours = distance_samples / speed_samples
        sfoc = 172.0
        base_fuel_tons = (power_kw * sfoc * voyage_hours / 1e6) * weather_penalty_samples * fuel_lhv_samples * efficiency_rating_samples
        
        noise = np.random.normal(1.0, 0.03, n_samples)
        y_fuel_tons = base_fuel_tons * noise
        
        X = np.column_stack([
            dwt_samples,
            cargo_ratio_samples,
            speed_samples,
            distance_samples,
            weather_penalty_samples,
            fuel_lhv_samples,
            efficiency_rating_samples
        ])
        
        self.model = GradientBoostingRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
        self.model.fit(X, y_fuel_tons)

    def predict_fuel_consumption(
        self,
        dwt: float,
        cargo_weight: float,
        speed_knots: float,
        distance_nm: float,
        weather_penalty: float,
        fuel_type: str,
        efficiency_rating: float = 1.0
    ) -> float:
        cargo_ratio = min(1.0, max(0.1, cargo_weight / max(dwt, 1.0)))
        fuel_lhv = self._fuel_energy_densities.get(fuel_type, 1.0)
        
        features = np.array([[
            dwt,
            cargo_ratio,
            speed_knots,
            distance_nm,
            weather_penalty,
            fuel_lhv,
            efficiency_rating
        ]])
        
        pred = self.model.predict(features)[0]
        return max(1.0, float(pred))

fuel_predictor = FuelPredictionModel()
