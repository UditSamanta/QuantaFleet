import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { 
  DollarSign, 
  Leaf, 
  TrendingDown, 
  Ship, 
  Percent, 
  PiggyBank, 
  Sparkles,
  BarChart2,
  PieChart,
  ArrowUpRight,
  ShieldAlert
} from 'lucide-react';

export const DashboardView = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await api.getDashboard();
        setData(res);
      } catch (err) {
        console.error("Error loading dashboard data:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="p-12 text-center">
        <div className="w-10 h-10 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <p className="text-sm font-medium text-slate-600">Loading Maritime Executive Dashboard...</p>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-6">
      
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-emerald-800 to-teal-900 rounded-2xl p-6 text-white shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs font-semibold text-emerald-300 uppercase tracking-wider mb-1">
            <Sparkles className="w-4 h-4 text-emerald-300" />
            <span>SIH26138 Green Fleet Telemetry</span>
          </div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight">
            Executive Fleet & Carbon Overview
          </h1>
          <p className="text-xs sm:text-sm text-emerald-100/80 mt-1 max-w-xl">
            Real-time multi-objective telemetry tracking voyage fuel expenditures, EU ETS carbon tax exposures, and quantum-optimized emissions reductions.
          </p>
        </div>

        <div className="flex items-center space-x-3 bg-white/10 backdrop-blur-md p-3 rounded-xl border border-white/10">
          <div className="w-10 h-10 rounded-lg bg-emerald-500/30 flex items-center justify-center text-emerald-200">
            <Percent className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xs text-emerald-200 font-medium">Green Fuel Adoption</div>
            <div className="text-xl font-bold">{data.green_fuel_adoption_pct}% of Active Fleet</div>
          </div>
        </div>
      </div>

      {/* 5 Core Dashboard KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        
        {/* Card 1: Total Fuel Cost */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm hover:border-slate-300 transition-colors">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Total Fuel Cost</span>
            <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <DollarSign className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 tracking-tight">
            {data.total_fuel_cost_ytd_usd}
          </div>
          <p className="text-[11px] text-emerald-600 font-medium mt-1 flex items-center">
            <TrendingDown className="w-3.5 h-3.5 mr-1" /> -12.4% vs Conventional Baseline
          </p>
        </div>

        {/* Card 2: Carbon Tax */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm hover:border-slate-300 transition-colors">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Carbon Tax (EU ETS)</span>
            <div className="w-8 h-8 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center">
              <Leaf className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 tracking-tight">
            {data.total_carbon_tax_ytd_usd}
          </div>
          <p className="text-[11px] text-slate-500 font-medium mt-1">
            Standard @ $85 / Ton CO₂
          </p>
        </div>

        {/* Card 3: CO2 Emissions */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm hover:border-slate-300 transition-colors">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">CO₂ Emissions</span>
            <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <Leaf className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-emerald-700 tracking-tight">
            {data.total_co2_emissions_ytd_tons}
          </div>
          <p className="text-[11px] text-emerald-600 font-medium mt-1 flex items-center">
            <TrendingDown className="w-3.5 h-3.5 mr-1" /> -26.8% Green Reduction
          </p>
        </div>

        {/* Card 4: Fleet Utilization */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm hover:border-slate-300 transition-colors">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Fleet Utilization</span>
            <div className="w-8 h-8 rounded-lg bg-slate-100 text-slate-700 flex items-center justify-center">
              <Ship className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 tracking-tight">
            {data.average_fleet_utilization_pct}%
          </div>
          <p className="text-[11px] text-slate-500 font-medium mt-1">
            {data.total_fleet_vessels} Cargo Ships In-Service
          </p>
        </div>

        {/* Card 5: Expected Savings */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm hover:border-slate-300 transition-colors">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Expected Savings</span>
            <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center">
              <PiggyBank className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-emerald-600 tracking-tight">
            {data.expected_green_savings_usd}
          </div>
          <p className="text-[11px] text-emerald-700 font-medium mt-1">
            Via QPSO Speed & Route Choice
          </p>
        </div>

      </div>

      {/* Charts & Visual Breakdowns */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Chart 1: Monthly Fuel Consumption & Transition */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-bold text-slate-900 text-base">Fuel Consumption Trend (Tons)</h3>
              <p className="text-xs text-slate-500">Conventional VLSFO vs Green Alternative Fuels (Jan - Aug)</p>
            </div>
            <BarChart2 className="w-5 h-5 text-emerald-600" />
          </div>

          <div className="space-y-3 pt-2">
            {data.fuel_trend.map((f, idx) => (
              <div key={idx} className="space-y-1">
                <div className="flex justify-between text-xs text-slate-600 font-medium">
                  <span className="w-10 font-bold">{f.month}</span>
                  <div className="flex space-x-4 text-[11px]">
                    <span className="text-slate-500">VLSFO: {f.conventional_vlsfo.toLocaleString()} T</span>
                    <span className="text-emerald-700 font-semibold">Green: {f.green_fuels.toLocaleString()} T</span>
                    <span className="text-emerald-600">+${(f.savings_usd/1000).toFixed(0)}k saved</span>
                  </div>
                </div>
                <div className="h-2.5 w-full bg-slate-100 rounded-full overflow-hidden flex">
                  <div 
                    style={{ width: `${(f.conventional_vlsfo / (f.conventional_vlsfo + f.green_fuels)) * 100}%` }}
                    className="bg-slate-400 h-full rounded-l-full"
                    title="Conventional VLSFO"
                  />
                  <div 
                    style={{ width: `${(f.green_fuels / (f.conventional_vlsfo + f.green_fuels)) * 100}%` }}
                    className="bg-emerald-500 h-full rounded-r-full"
                    title="Green Clean Fuels"
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="flex items-center justify-center space-x-6 mt-4 pt-3 border-t border-slate-100 text-xs text-slate-600">
            <div className="flex items-center space-x-1.5">
              <span className="w-3 h-3 rounded-full bg-slate-400" />
              <span>Conventional VLSFO</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="w-3 h-3 rounded-full bg-emerald-500" />
              <span>Green Clean Fuels (LNG, Bio-Methanol, Ammonia, H2)</span>
            </div>
          </div>
        </div>

        {/* Chart 2: Cost Breakdown & Vessel Distribution */}
        <div className="space-y-6">
          
          {/* Voyage Cost Breakdown */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="font-bold text-slate-900 text-base">Voyage Cost Breakdown</h3>
                <p className="text-xs text-slate-500">Components contributing to Total Voyage Expenditure</p>
              </div>
              <PieChart className="w-5 h-5 text-emerald-600" />
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {data.cost_breakdown.map((c, idx) => (
                <div key={idx} className="bg-slate-50 p-3.5 rounded-xl border border-slate-100">
                  <div className="text-xs text-slate-500 font-medium truncate">{c.name}</div>
                  <div className="text-lg font-bold text-slate-900 mt-0.5">{c.amount}</div>
                  <div className="text-xs font-semibold text-emerald-600">{c.value}% share</div>
                </div>
              ))}
            </div>
          </div>

          {/* Active Fleet Breakdown */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
            <h3 className="font-bold text-slate-900 text-base mb-3">Vessel Category Distribution</h3>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {data.vessel_type_distribution.map((v, idx) => (
                <div key={idx} className="bg-emerald-50/60 p-3 rounded-xl border border-emerald-100">
                  <div className="text-xs text-emerald-900 font-semibold">{v.type}</div>
                  <div className="text-xl font-bold text-emerald-700 mt-1">{v.count} Ships</div>
                  <div className="text-[11px] text-slate-500">{v.share} of Fleet</div>
                </div>
              ))}
            </div>
          </div>

        </div>

      </div>

    </div>
  );
};
