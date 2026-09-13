import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Compass, Leaf, LogOut } from 'lucide-react';

export const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-600 flex items-center justify-center text-white shadow-sm shadow-emerald-200">
              <Compass className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center space-x-1.5">
                <span className="font-bold text-xl text-slate-900 tracking-tight">Quantum<span className="text-emerald-600">Fleet</span></span>
                <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                  <Leaf className="w-2.5 h-2.5 mr-0.5" /> GREEN
                </span>
              </div>
              <p className="text-[11px] text-slate-500 hidden sm:block">Intelligent Fuel & Voyage Optimization</p>
            </div>
          </div>

          {user && (
            <div className="flex items-center space-x-4">
              <div className="text-right hidden sm:block">
                <div className="text-sm font-semibold text-slate-800">{user.full_name}</div>
                <div className="text-xs text-slate-500 flex items-center justify-end space-x-1">
                  <span>{user.company_name}</span>
                  <span>•</span>
                  <span className="text-emerald-600 font-medium">{user.role}</span>
                </div>
              </div>

              <div className="h-8 w-px bg-slate-200 hidden sm:block" />

              <button
                onClick={logout}
                title="Log Out"
                className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-sm font-medium text-slate-600 hover:text-red-600 hover:bg-red-50 border border-slate-200 transition-colors cursor-pointer"
              >
                <LogOut className="w-4 h-4" />
                <span className="hidden md:inline">Sign Out</span>
              </button>
            </div>
          )}

        </div>
      </div>
    </header>
  );
};
