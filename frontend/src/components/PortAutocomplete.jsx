import React, { useState, useEffect, useRef } from 'react';
import { api } from '../services/api';
import { Anchor, ChevronDown, MapPin } from 'lucide-react';

export const PortAutocomplete = ({
  label,
  placeholder,
  value,
  onChange,
  required = false
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState(value || '');
  const [ports, setPorts] = useState([]);
  const [loading, setLoading] = useState(false);
  const wrapperRef = useRef(null);

  useEffect(() => {
    setSearchTerm(value || '');
  }, [value]);

  useEffect(() => {
    let active = true;
    const fetchPorts = async () => {
      setLoading(true);
      try {
        const data = await api.getPorts(searchTerm);
        if (active) {
          setPorts(data);
        }
      } catch (err) {
        console.error("Error fetching ports:", err);
      } finally {
        if (active) setLoading(false);
      }
    };

    const timeoutId = setTimeout(fetchPorts, 200);
    return () => {
      active = false;
      clearTimeout(timeoutId);
    };
  }, [searchTerm]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelectPort = (port) => {
    setSearchTerm(port.name);
    onChange(port.name);
    setIsOpen(false);
  };

  return (
    <div className="relative" ref={wrapperRef}>
      <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1.5">
        {label} {required && <span className="text-red-500">*</span>}
      </label>

      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
          <Anchor className="w-4 h-4 text-emerald-600" />
        </div>

        <input
          type="text"
          value={searchTerm}
          onChange={(e) => {
            setSearchTerm(e.target.value);
            onChange(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          placeholder={placeholder}
          required={required}
          className="w-full pl-10 pr-10 py-2.5 bg-white border border-slate-300 rounded-xl text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-shadow shadow-sm"
        />

        <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none text-slate-400">
          <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
        </div>
      </div>

      {isOpen && (
        <div className="absolute z-50 left-0 right-0 mt-1.5 max-h-64 overflow-y-auto bg-white border border-slate-200 rounded-xl shadow-xl py-1 text-sm">
          {loading ? (
            <div className="px-4 py-3 text-xs text-slate-400 flex items-center justify-center space-x-2">
              <div className="w-3.5 h-3.5 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
              <span>Searching global ports...</span>
            </div>
          ) : ports.length === 0 ? (
            <div className="px-4 py-3 text-xs text-slate-400 text-center">
              No matching ports found. Type a port or country name.
            </div>
          ) : (
            ports.map((port) => (
              <button
                key={port.id}
                type="button"
                onClick={() => handleSelectPort(port)}
                className="w-full px-3.5 py-2.5 text-left hover:bg-emerald-50/80 flex items-center justify-between transition-colors border-b border-slate-50 last:border-0 cursor-pointer"
              >
                <div className="flex items-center space-x-2.5 truncate">
                  <MapPin className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0" />
                  <div className="truncate">
                    <span className="font-medium text-slate-800">{port.name}</span>
                    <span className="text-xs text-slate-500 ml-1.5">({port.country})</span>
                  </div>
                </div>
                <span className="text-[11px] font-mono px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 border border-slate-200 flex-shrink-0 ml-2">
                  {port.code}
                </span>
              </button>
            ))
          )}
        </div>
      )}
    </div>
  );
};
