# QuantumFleet — Quantum-Inspired Fuel Consumption Prediction & Green Fleet Optimization

QuantumFleet is a full-stack maritime decision-support platform that helps shipping fleet operators cut fuel costs and carbon emissions through data-driven voyage planning. It pairs a physics-informed machine learning model for fuel prediction with a **Quantum Particle Swarm Optimization (QPSO)** engine to generate Pareto-optimal recommendations across speed, route, and fuel trade-offs — delivered in sub-second execution time.

Maritime shipping drives most of global trade but also produces massive greenhouse gas emissions. With regulations like the EU Emissions Trading System (ETS) and the IMO Carbon Intensity Indicator (CII) now taxing and scoring vessels on emissions, operators relying on legacy noon-report spreadsheets face rising costs and compliance risk. QuantumFleet solves this by combining naval hydrodynamics with a quantum-inspired optimizer that avoids the local-minima traps common in classical PSO and genetic algorithms, enabling more robust, globally optimal fleet dispatch decisions.

## ✨ Key Features

- 🚢 **Fleet Management** — track and manage 100+ vessels with detailed specifications
- 🧠 **ML Fuel Prediction** — gradient-boosted models (XGBoost / Random Forest / Linear) trained on an Admiralty power-law hydrodynamic model
- ⚛️ **QPSO Optimizer** — delta-potential-well-based quantum optimizer for Pareto-optimal voyage planning
- 🌊 **Weather-Aware Routing** — factors in wind speed and wave height for drag-adjusted fuel estimates
- 📊 **Emission & Carbon Tax Analytics** — IMO emission factor calculations with EU ETS cost projections
- 🗺️ **Interactive Voyage Planning** — map-based route visualization with port autocomplete
- 📈 **Executive Dashboard & AI Insights** — fleet KPIs and optimizer benchmarking
- 🔐 **Authentication** — JWT-based multi-user login

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python), SQLAlchemy, SQLite/PostgreSQL |
| ML Engine | scikit-learn / XGBoost fuel prediction models |
| Frontend | React 18, Vite, Tailwind CSS, Leaflet |
| Optimization | Custom Quantum-Inspired PSO implementation |
| Deployment | Docker & docker-compose |

## 🏆 Background

Originally built for **Smart India Hackathon 2026** (Problem Statement **SIH26138**, Smart Vehicles/Logistics), QuantumFleet demonstrates how quantum-inspired algorithms and machine learning can be applied to solve real-world green logistics challenges in the maritime industry.
