import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Ship, Search, Filter, Fuel, Flag, Anchor, Gauge, Calendar, ShieldCheck } from 'lucide-react';

export const FleetManagementView = () => {
  const [vessels, setVessels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedFuel, setSelectedFuel] = useState('All');

  const categories = ['All', 'Container', 'Bulk', 'Liquid', 'Refrigerated', 'General'];
  const fuels = ['All', 'Bio-Methanol', 'LNG', 'Ammonia', 'Hydrogen', 'VLSFO', 'LSMGO', 'Biofuel (B30)'];

  useEffect(() => {
    const fetchVessels = async () => {
      setLoading(true);
      try {
        const data = await api.getVessels({
          search: searchTerm,
          category: selectedCategory,
          fuel: selectedFuel,
        });
        setVessels(data);
      } catch (err) {
        console.error("Error fetching fleet:", err);
      } finally {
        setLoading(false);
      }
    };

    const timer = setTimeout(fetchVessels, 200);
    return () => clearTimeout(timer);
  }, [searchTerm, selectedCategory, selectedFuel]);

  return (
    <div className="space-y-6">
      
      {/* Header & Filter Controls */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-100">
          <div>
            <h2 className="text-xl font-bold text-slate-900 tracking-tight flex items-center space-x-2">
              <span>Maritime Fleet Registry</span>
              <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
                {vessels.length} Vessels Loaded
              </span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
              Comprehensive Equasis-integrated vessel inventory with multi-fuel compatibility and energy efficiency index ratings.
            </p>
          </div>
        </div>

        {/* Filters */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-5">
          {/* Search Box */}
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              <Search className="w-4 h-4 text-emerald-600" />
            </div>
            <input
              type="text"
              placeholder="Search by ship name, IMO, or type..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white transition-all"
            />
          </div>

          {/* Category Filter */}
          <div>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white transition-all cursor-pointer"
            >
              {categories.map((cat) => (
                <option key={cat} value={cat}>Category: {cat}</option>
              ))}
            </select>
          </div>

          {/* Fuel Filter */}
          <div>
            <select
              value={selectedFuel}
              onChange={(e) => setSelectedFuel(e.target.value)}
              className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white transition-all cursor-pointer"
            >
              {fuels.map((f) => (
                <option key={f} value={f}>Primary Fuel: {f}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Vessels Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-12 text-center">
            <div className="w-8 h-8 border-3 border-emerald-600 border-t-transparent rounded-full animate-spin mx-auto mb-2" />
            <span className="text-xs text-slate-500">Querying maritime vessel registry...</span>
          </div>
        ) : vessels.length === 0 ? (
          <div className="p-12 text-center text-slate-400 text-sm">
            No vessels found matching your filter criteria.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-sm">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                  <th className="py-3 px-4">Vessel Name & IMO</th>
                  <th className="py-3 px-4">Ship Class / Type</th>
                  <th className="py-3 px-4">Deadweight (DWT)</th>
                  <th className="py-3 px-4">Primary / Multi-Fuels</th>
                  <th className="py-3 px-4">Speed</th>
                  <th className="py-3 px-4">Built / Flag</th>
                  <th className="py-3 px-4">Efficiency</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {vessels.map((v) => (
                  <tr key={v.id} className="hover:bg-emerald-50/40 transition-colors">
                    <td className="py-3.5 px-4">
                      <div className="font-bold text-slate-900">{v.name}</div>
                      <div className="text-xs font-mono text-slate-500">IMO: {v.imo_number}</div>
                    </td>

                    <td className="py-3.5 px-4 text-slate-700 font-medium">
                      {v.ship_type}
                    </td>

                    <td className="py-3.5 px-4">
                      <div className="font-semibold text-slate-900">{v.dwt.toLocaleString()} DWT</div>
                      <div className="text-xs text-slate-500">Cap: {v.capacity_tons.toLocaleString()} T</div>
                    </td>

                    <td className="py-3.5 px-4">
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 mb-1">
                        <Fuel className="w-3 h-3 mr-1 text-emerald-600" />
                        {v.primary_fuel}
                      </span>
                      <div className="text-[11px] text-slate-400 truncate max-w-[160px]">
                        Alt: {(v.compatible_fuels || []).filter(f => f !== v.primary_fuel).join(', ') || 'None'}
                      </div>
                    </td>

                    <td className="py-3.5 px-4">
                      <span className="font-semibold text-slate-800">{v.service_speed} kts</span>
                    </td>

                    <td className="py-3.5 px-4">
                      <div className="text-slate-800 font-medium">{v.flag_country}</div>
                      <div className="text-xs text-slate-500">Yr: {v.year_built}</div>
                    </td>

                    <td className="py-3.5 px-4">
                      <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-bold ${
                        v.efficiency_rating <= 0.88 
                          ? 'bg-emerald-100 text-emerald-800' 
                          : v.efficiency_rating <= 1.0 
                          ? 'bg-slate-100 text-slate-700' 
                          : 'bg-amber-100 text-amber-800'
                      }`}>
                        {v.efficiency_rating}x
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

    </div>
  );
};
