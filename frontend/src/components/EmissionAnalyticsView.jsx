import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Leaf, DollarSign, ShieldAlert, Sparkles, PieChart, FileText, ArrowRight } from 'lucide-react';

export const EmissionAnalyticsView = () => {
  const [fuelConsumed, setFuelConsumed] = useState(1500);
  const [fuelType, setFuelType] = useState('Bio-Methanol');
  const [taxRate, setTaxRate] = useState(85.0);
  const [portFees, setPortFees] = useState(45000);

  const [emissionData, setEmissionData] = useState(null);
  const [taxData, setTaxData] = useState(null);

  const fuels = [
    { id: 'Bio-Methanol', name: 'Bio-Methanol', factor: 0.450, taxMultiplier: '85% Savings' },
    { id: 'LNG', name: 'LNG', factor: 2.750, taxMultiplier: 'Low Particulates' },
    { id: 'Ammonia', name: 'Ammonia', factor: 0.050, taxMultiplier: 'Zero Direct CO2' },
    { id: 'Hydrogen', name: 'Hydrogen', factor: 0.000, taxMultiplier: 'Zero Emission' },
    { id: 'VLSFO', name: 'VLSFO', factor: 3.114, taxMultiplier: 'High Carbon Tax' },
    { id: 'LSMGO', name: 'LSMGO', factor: 3.206, taxMultiplier: 'High Carbon Tax' },
    { id: 'Biofuel (B30)', name: 'Biofuel (B30)', factor: 2.180, taxMultiplier: '30% Blend' },
  ];

  useEffect(() => {
    let active = true;
    const compute = async () => {
      try {
        const em = await api.calculateEmission({
          fuel_consumed_tons: parseFloat(fuelConsumed),
          fuel_type: fuelType
        });
        
        // Approximate fuel price per ton
        const pMap = { "Bio-Methanol": 510, "LNG": 540, "Ammonia": 740, "Hydrogen": 1850, "VLSFO": 615, "LSMGO": 790, "Biofuel (B30)": 780 };
        const fuelCost = parseFloat(fuelConsumed) * (pMap[fuelType] || 620);

        const tx = await api.calculateTax({
          co2_emissions_tons: em.co2_emissions_tons,
          fuel_cost_usd: fuelCost,
          port_charges_usd: parseFloat(portFees),
          tax_rate_usd_per_ton: parseFloat(taxRate)
        });

        if (active) {
          setEmissionData(em);
          setTaxData(tx);
        }
      } catch (err) {
        console.error("Error computing emissions:", err);
      }
    };

    compute();
    return () => { active = false; };
  }, [fuelConsumed, fuelType, taxRate, portFees]);

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-100">
          <div>
            <h2 className="text-xl font-bold text-slate-900 tracking-tight flex items-center space-x-2">
              <Leaf className="w-5 h-5 text-emerald-600" />
              <span>IMO GHG & EU ETS Carbon Tax Engine</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
              Official IMO Greenhouse Gas Study 4 emission factors and compliance carbon taxation simulator.
            </p>
          </div>
          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-emerald-100 text-emerald-800">
            EU ETS Maritime Directive Active
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Controls (Left 6 Cols) */}
        <div className="lg:col-span-6 bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-5">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-700">Voyage Fuel & Taxation Parameters</h3>

          <div>
            <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
              <span>Fuel Consumed (Tons)</span>
              <span className="text-emerald-700 font-bold">{fuelConsumed.toLocaleString()} Tons</span>
            </div>
            <input
              type="range"
              min="100"
              max="5000"
              step="50"
              value={fuelConsumed}
              onChange={(e) => setFuelConsumed(e.target.value)}
              className="w-full accent-emerald-600 cursor-pointer"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-slate-600 mb-2">Select Bunkered Fuel Type</label>
            <div className="grid grid-cols-2 gap-2">
              {fuels.map((f) => (
                <button
                  key={f.id}
                  type="button"
                  onClick={() => setFuelType(f.id)}
                  className={`p-3 rounded-xl border text-left text-xs transition-all cursor-pointer ${
                    fuelType === f.id
                      ? 'border-emerald-600 bg-emerald-50/90 text-emerald-950 ring-1 ring-emerald-600 font-bold'
                      : 'border-slate-200 hover:bg-slate-50 text-slate-700 font-medium'
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <span>{f.name}</span>
                    <span className="text-[10px] text-emerald-700 font-semibold">{f.factor}x</span>
                  </div>
                  <span className="text-[10px] text-slate-500">{f.taxMultiplier}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
            <div>
              <label className="block text-xs font-semibold uppercase text-slate-600 mb-1">Carbon Tax Rate ($ / Ton CO₂)</label>
              <input
                type="number"
                value={taxRate}
                onChange={(e) => setTaxRate(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-semibold text-slate-800"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase text-slate-600 mb-1">Port & Canal Dues (USD)</label>
              <input
                type="number"
                value={portFees}
                onChange={(e) => setPortFees(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-semibold text-slate-800"
              />
            </div>
          </div>
        </div>

        {/* Results & Breakdown (Right 6 Cols) */}
        <div className="lg:col-span-6 space-y-6">
          
          {/* Emissions Breakdown Card */}
          {emissionData && (
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
              <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
                <h3 className="font-bold text-slate-900 text-sm uppercase tracking-wider">Atmospheric Greenhouse Impact</h3>
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
                  emissionData.emission_badge === 'green' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
                }`}>
                  {emissionData.emission_badge.toUpperCase()} IMPACT
                </span>
              </div>

              <div className="grid grid-cols-3 gap-3 text-center">
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                  <div className="text-xs text-slate-500 font-medium">CO₂ Emissions</div>
                  <div className="text-xl font-extrabold text-slate-900 mt-1">{emissionData.co2_emissions_tons.toLocaleString()}</div>
                  <div className="text-[10px] text-slate-400">Metric Tons</div>
                </div>

                <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                  <div className="text-xs text-slate-500 font-medium">NOₓ Emissions</div>
                  <div className="text-xl font-extrabold text-slate-900 mt-1">{emissionData.nox_emissions_kg.toLocaleString()}</div>
                  <div className="text-[10px] text-slate-400">Kilograms</div>
                </div>

                <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                  <div className="text-xs text-slate-500 font-medium">SOₓ Emissions</div>
                  <div className="text-xl font-extrabold text-slate-900 mt-1">{emissionData.sox_emissions_kg.toLocaleString()}</div>
                  <div className="text-[10px] text-slate-400">Kilograms</div>
                </div>
              </div>
            </div>
          )}

          {/* Carbon Tax & Total Voyage Cost Card */}
          {taxData && (
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
              <h3 className="font-bold text-slate-900 text-sm uppercase tracking-wider mb-4">
                Total Voyage Cost Structure
              </h3>

              <div className="space-y-3">
                <div className="flex justify-between items-center text-sm p-3 rounded-xl bg-slate-50 border border-slate-100">
                  <span className="text-slate-600 font-medium">Bunker Fuel Cost</span>
                  <span className="font-bold text-slate-900">${taxData.fuel_cost_usd.toLocaleString()}</span>
                </div>

                <div className="flex justify-between items-center text-sm p-3 rounded-xl bg-amber-50/70 border border-amber-100">
                  <span className="text-amber-900 font-semibold">EU ETS Carbon Tax Penalty</span>
                  <span className="font-extrabold text-amber-700">${taxData.carbon_tax_cost_usd.toLocaleString()}</span>
                </div>

                <div className="flex justify-between items-center text-sm p-3 rounded-xl bg-slate-50 border border-slate-100">
                  <span className="text-slate-600 font-medium">Port Charges & Canal Dues</span>
                  <span className="font-bold text-slate-900">${taxData.port_charges_usd.toLocaleString()}</span>
                </div>

                <div className="flex justify-between items-center text-base p-4 rounded-xl bg-emerald-800 text-white font-bold mt-4 shadow-sm">
                  <span>Total Calculated Voyage Cost</span>
                  <span className="text-xl font-extrabold text-emerald-200">${taxData.total_voyage_cost_usd.toLocaleString()}</span>
                </div>
              </div>
            </div>
          )}

        </div>

      </div>

    </div>
  );
};
