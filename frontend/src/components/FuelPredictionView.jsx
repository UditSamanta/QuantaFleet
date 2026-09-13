import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Cpu, Gauge, Fuel, Wind, Waves, Eye, DollarSign, Leaf, Sparkles, CheckCircle } from 'lucide-react';

export const FuelPredictionView = () => {
  const [distance, setDistance] = useState(6450);
  const [cargoWeight, setCargoWeight] = useState(48000);
  const [speed, setSpeed] = useState(15.5);
  const [windSpeed, setWindSpeed] = useState(14.0);
  const [waveHeight, setWaveHeight] = useState(1.8);
  const [visibility, setVisibility] = useState(10.0);
  const [fuelType, setFuelType] = useState('Bio-Methanol');
  const [shipType, setShipType] = useState('Container - Panamax (5,000 TEU)');

  const [predictionResult, setPredictionResult] = useState(null);
  const [modelMetrics, setModelMetrics] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fetch model comparison metrics on mount
  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const m = await api.getModelMetrics();
        setModelMetrics(m);
      } catch (err) {
        console.error("Error fetching model metrics:", err);
      }
    };
    fetchMetrics();
  }, []);

  // Run prediction on parameters change
  useEffect(() => {
    let active = true;
    const runPredict = async () => {
      setLoading(true);
      try {
        const res = await api.predictFuel({
          distance_nm: parseFloat(distance),
          cargo_weight_tons: parseFloat(cargoWeight),
          speed_knots: parseFloat(speed),
          wind_speed_knots: parseFloat(windSpeed),
          wave_height_m: parseFloat(waveHeight),
          visibility_nm: parseFloat(visibility),
          fuel_type: fuelType,
          ship_type: shipType
        });
        if (active) setPredictionResult(res);
      } catch (err) {
        console.error("Prediction error:", err);
      } finally {
        if (active) setLoading(false);
      }
    };

    const timer = setTimeout(runPredict, 250);
    return () => {
      active = false;
      clearTimeout(timer);
    };
  }, [distance, cargoWeight, speed, windSpeed, waveHeight, visibility, fuelType, shipType]);

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-100">
          <div>
            <h2 className="text-xl font-bold text-slate-900 tracking-tight flex items-center space-x-2">
              <Cpu className="w-5 h-5 text-emerald-600" />
              <span>Machine Learning Fuel Consumption Predictor</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
              Interactive physics-informed naval regressor trained on EU MRV validated voyage datasets.
            </p>
          </div>
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">
            <Sparkles className="w-3.5 h-3.5 mr-1" /> XGBoost Regressor Active
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Controls Section (Left 7 Cols) */}
        <div className="lg:col-span-7 bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-5">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-700">Voyage & Environmental Parameters</h3>

          {/* Distance & Cargo Weight */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                <span>Voyage Distance (NM)</span>
                <span className="text-emerald-700 font-bold">{distance.toLocaleString()} NM</span>
              </div>
              <input 
                type="range" 
                min="500" 
                max="15000" 
                step="100" 
                value={distance} 
                onChange={(e) => setDistance(e.target.value)}
                className="w-full accent-emerald-600 cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                <span>Cargo Weight (Tons)</span>
                <span className="text-emerald-700 font-bold">{cargoWeight.toLocaleString()} Tons</span>
              </div>
              <input 
                type="range" 
                min="5000" 
                max="220000" 
                step="1000" 
                value={cargoWeight} 
                onChange={(e) => setCargoWeight(e.target.value)}
                className="w-full accent-emerald-600 cursor-pointer"
              />
            </div>
          </div>

          {/* Speed & Wind */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                <span>Operating Speed (Knots)</span>
                <span className="text-emerald-700 font-bold">{speed} kts</span>
              </div>
              <input 
                type="range" 
                min="10.0" 
                max="24.0" 
                step="0.1" 
                value={speed} 
                onChange={(e) => setSpeed(e.target.value)}
                className="w-full accent-emerald-600 cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                <span>Wind Speed (Knots)</span>
                <span className="text-emerald-700 font-bold">{windSpeed} kts</span>
              </div>
              <input 
                type="range" 
                min="4.0" 
                max="40.0" 
                step="0.5" 
                value={windSpeed} 
                onChange={(e) => setWindSpeed(e.target.value)}
                className="w-full accent-emerald-600 cursor-pointer"
              />
            </div>
          </div>

          {/* Wave Height & Visibility */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                <span>Wave Height (Swell in Meters)</span>
                <span className="text-emerald-700 font-bold">{waveHeight} m</span>
              </div>
              <input 
                type="range" 
                min="0.5" 
                max="6.0" 
                step="0.1" 
                value={waveHeight} 
                onChange={(e) => setWaveHeight(e.target.value)}
                className="w-full accent-emerald-600 cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                <span>Visibility (Nautical Miles)</span>
                <span className="text-emerald-700 font-bold">{visibility} NM</span>
              </div>
              <input 
                type="range" 
                min="2.0" 
                max="20.0" 
                step="0.5" 
                value={visibility} 
                onChange={(e) => setVisibility(e.target.value)}
                className="w-full accent-emerald-600 cursor-pointer"
              />
            </div>
          </div>

          {/* Fuel & Ship Type Selectors */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
            <div>
              <label className="block text-xs font-semibold uppercase text-slate-600 mb-1">Fuel Type</label>
              <select
                value={fuelType}
                onChange={(e) => setFuelType(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-semibold text-slate-800 focus:ring-2 focus:ring-emerald-500 cursor-pointer"
              >
                <option value="Bio-Methanol">Bio-Methanol (Clean e-Fuel)</option>
                <option value="LNG">LNG (Liquefied Natural Gas)</option>
                <option value="Ammonia">Green Ammonia (Zero-Carbon)</option>
                <option value="Hydrogen">Liquid Hydrogen (Zero-Carbon)</option>
                <option value="VLSFO">VLSFO (0.5% Low Sulfur Fuel Oil)</option>
                <option value="LSMGO">LSMGO (Marine Gas Oil)</option>
                <option value="Biofuel (B30)">Biofuel B30 Blend</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase text-slate-600 mb-1">Vessel Class</label>
              <select
                value={shipType}
                onChange={(e) => setShipType(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-semibold text-slate-800 focus:ring-2 focus:ring-emerald-500 cursor-pointer"
              >
                <option value="Container - Panamax (5,000 TEU)">Container - Panamax (5,000 TEU)</option>
                <option value="Container - Ultra Large (24,000 TEU)">Container - Ultra Large (24,000 TEU)</option>
                <option value="Bulk Carrier - Panamax Class">Bulk Carrier - Panamax Class</option>
                <option value="Bulk Carrier - Capesize Class">Bulk Carrier - Capesize Class</option>
                <option value="Tanker - VLCC Class">Tanker - VLCC Class</option>
                <option value="Reefer - Arctic Pioneer">Reefer - Arctic Pioneer</option>
              </select>
            </div>
          </div>
        </div>

        {/* Prediction Results & Model Comparison (Right 5 Cols) */}
        <div className="lg:col-span-5 space-y-6">
          
          {/* Main ML Output Card */}
          <div className="bg-emerald-900 text-white rounded-2xl p-6 shadow-md relative overflow-hidden">
            <div className="text-xs font-semibold text-emerald-300 uppercase tracking-wider mb-1">
              Predicted Total Fuel Consumption
            </div>
            
            <div className="flex items-baseline space-x-2 my-2">
              <span className="text-4xl sm:text-5xl font-extrabold tracking-tight">
                {predictionResult ? predictionResult.predicted_fuel_consumed_tons.toLocaleString() : '---'}
              </span>
              <span className="text-lg font-semibold text-emerald-200">Tons</span>
            </div>

            {predictionResult && (
              <div className="grid grid-cols-2 gap-3 pt-3 border-t border-emerald-800/80 text-xs">
                <div>
                  <span className="text-emerald-300">Daily Fuel Rate:</span>
                  <div className="text-base font-bold">{predictionResult.daily_fuel_rate_tons_per_day} T / Day</div>
                </div>
                <div>
                  <span className="text-emerald-300">Voyage Duration:</span>
                  <div className="text-base font-bold">{(predictionResult.total_travel_hours / 24).toFixed(1)} Days</div>
                </div>
                <div>
                  <span className="text-emerald-300">Est. Fuel Cost:</span>
                  <div className="text-base font-bold text-emerald-200">${(predictionResult.estimated_fuel_cost_usd / 1000).toFixed(0)}k</div>
                </div>
                <div>
                  <span className="text-emerald-300">CO₂ Emissions:</span>
                  <div className="text-base font-bold text-emerald-200">{predictionResult.estimated_co2_emissions_tons.toLocaleString()} T</div>
                </div>
              </div>
            )}
          </div>

          {/* Model Architecture Comparison Table */}
          {predictionResult && predictionResult.all_models_comparison && (
            <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
                Architectural Model Comparison
              </h4>
              <div className="space-y-2.5">
                {Object.entries(predictionResult.all_models_comparison).map(([mName, val]) => (
                  <div key={mName} className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-100 text-xs">
                    <div className="flex items-center space-x-2">
                      <CheckCircle className={`w-4 h-4 ${mName.includes('XGBoost') ? 'text-emerald-600' : 'text-slate-400'}`} />
                      <span className="font-semibold text-slate-800">{mName}</span>
                    </div>
                    <span className="font-mono font-bold text-slate-900">{val.toLocaleString()} T</span>
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>

      </div>

    </div>
  );
};
