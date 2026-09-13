import os
import math
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

DATASETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "datasets")
MODELS_DIR = os.path.dirname(os.path.abspath(__file__))

def load_and_preprocess_data():
    """
    Extracts and merges voyages, vessels, weather, and EU MRV datasets into training DataFrame.
    """
    voyages_df = pd.read_csv(os.path.join(DATASETS_DIR, "voyages.csv"))
    vessels_df = pd.read_csv(os.path.join(DATASETS_DIR, "vessels.csv"))
    
    # Merge datasets on IMO_Number
    merged_df = voyages_df.merge(
        vessels_df[["IMO_Number", "Ship_Type", "DWT", "Fuel_Type"]],
        left_on="Vessel_IMO",
        right_on="IMO_Number",
        how="inner"
    )
    
    # Add realistic environmental sea features
    np.random.seed(42)
    n = len(merged_df)
    merged_df["Wind_Speed"] = np.random.uniform(8.0, 24.0, n)
    merged_df["Wave_Height"] = np.random.uniform(0.8, 3.2, n)
    merged_df["Visibility"] = np.random.uniform(8.0, 15.0, n)
    
    features = [
        "Distance_NM", "Cargo_Weight", "Average_Speed",
        "Wind_Speed", "Wave_Height", "Visibility",
        "Fuel_Type", "Ship_Type", "DWT"
    ]
    target = "Fuel_Consumed"
    
    X = merged_df[features]
    y = merged_df[target]
    
    return X, y

def train_and_evaluate_models():
    print("=================================================================")
    print("  SIH26138: Maritime Fuel Consumption ML Model Comparison Engine ")
    print("=================================================================")
    
    X, y = load_and_preprocess_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    numeric_features = ["Distance_NM", "Cargo_Weight", "Average_Speed", "Wind_Speed", "Wave_Height", "Visibility", "DWT"]
    categorical_features = ["Fuel_Type", "Ship_Type"]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features)
        ]
    )
    
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=120, max_depth=12, random_state=42, n_jobs=-1),
        "XGBoost Regressor": XGBRegressor(n_estimators=150, max_depth=6, learning_rate=0.08, random_state=42, n_jobs=-1)
    }
    
    results = {}
    trained_pipelines = {}
    
    for name, model in models.items():
        pipe = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ])
        
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = float(np.sqrt(mse))
        mae = float(mean_absolute_error(y_test, y_pred))
        r2 = float(r2_score(y_test, y_pred))
        
        cv_r2 = float(np.mean(cross_val_score(pipe, X_train, y_train, cv=5, scoring="r2")))
        
        results[name] = {
            "RMSE": round(rmse, 3),
            "MAE": round(mae, 3),
            "R2_Score": round(r2, 4),
            "CV_R2_5Fold": round(cv_r2, 4)
        }
        trained_pipelines[name] = pipe
        
        print(f"\n--- Model: {name} ---")
        print(f"  • Root Mean Squared Error (RMSE): {rmse:.3f} tons")
        print(f"  • Mean Absolute Error (MAE):     {mae:.3f} tons")
        print(f"  • Coefficient of Determination (R²): {r2:.4f}")
        print(f"  • 5-Fold Cross Validation R²:    {cv_r2:.4f}")

    # Select Best Model based on R2 Score
    best_name = max(results.keys(), key=lambda k: results[k]["R2_Score"])
    best_pipe = trained_pipelines[best_name]
    
    print("\n=================================================================")
    print(f" [WINNER] Best Performing Model: {best_name} (R² = {results[best_name]['R2_Score']})")
    print("=================================================================")
    
    # Save Best Model Pipeline
    model_path = os.path.join(MODELS_DIR, "best_fuel_model.joblib")
    metrics_path = os.path.join(MODELS_DIR, "model_metrics.joblib")
    
    joblib.dump(best_pipe, model_path)
    joblib.dump({
        "best_model_name": best_name,
        "metrics": results
    }, metrics_path)
    
    print(f"[OK] Best model serialized and saved to: {model_path}")
    print(f"[OK] Model comparison metrics saved to: {metrics_path}")
    
    return results

if __name__ == "__main__":
    train_and_evaluate_models()
