# QuantumFleet: System Architecture & Engineering Design (SIH26138)

**Team**: Vanakkam  
**Theme**: Smart Vehicles / Logistics  
**Problem Statement**: SIH26138 – Quantum-Inspired Fuel Consumption Prediction and Green Fleet Optimization

---

## 1. High-Level System Architecture

```mermaid
graph TD
    subgraph "External Maritime Datasets"
        D1[Equasis Vessels CSV] --> ETL[Python ETL & Validation Engine]
        D2[Kaggle/Datalastic Voyages CSV] --> ETL
        D3[EU MRV Fuel Consumption] --> ETL
        D4[OpenWeather / Open-Meteo] --> ETL
        D5[Ship & Bunker Fuel Prices] --> ETL
        D6[World Port Index] --> ETL
        D7[IMO Emission Factors] --> ETL
    end

    subgraph "Persistent Storage Layer"
        ETL --> PG[(PostgreSQL Database / SQLite)]
    end

    subgraph "Backend Intelligence Engine (FastAPI on Port 8001)"
        PG --> ML[Fuel Consumption ML Pipeline<br/>XGBoost / RF / Linear]
        PG --> EM[IMO Emission & Carbon Tax Engine]
        PG --> DIST[Maritime Haversine & Lane Distance]
        PG --> WX[Ocean Weather & Drag Penalty Engine]
        
        ML & EM & DIST & WX --> QPSO[Quantum Particle Swarm Optimizer<br/>Delta-Potential Well Model]
        QPSO --> CACHE[Pareto Solutions Cache]
    end

    subgraph "Client Presentation Layer (React + Tailwind on Port 5173)"
        CACHE --> API[/api/recommend & /api/get-dashboard]
        API --> UI1[Executive Dashboard]
        API --> UI2[Voyage Planning & QPSO]
        API --> UI3[Fleet Management 105 Ships]
        API --> UI4[Fuel ML Simulator]
        API --> UI5[Emission Analytics]
        API --> UI6[AI Insights & Benchmarks]
    end
```

---

## 2. Core Mathematical Formulations

### 2.1 Physics-Informed Naval Hydrodynamic Power Model
Under Admiralty Law of Naval Architecture:
\[
P = \frac{\Delta^{2/3} \cdot V^3}{C_{\text{adm}}} \cdot \eta_{\text{weather}} \cdot \eta_{\text{fuel}}
\]
Where:
- \(\Delta\): Vessel Displacement in metric tons (\(\text{DWT} \times (0.25 + \frac{\text{Cargo}}{\text{DWT}})\))
- \(V\): Service Speed in knots
- \(C_{\text{adm}}\): Admiralty Coefficient (typically \(450 - 600\))
- \(\eta_{\text{weather}}\): Dynamic drag multiplier derived from wind speed and significant wave height (\(1.0 + \frac{W_{\text{wind}}}{100} + \frac{H_{\text{wave}}}{25}\))
- \(\eta_{\text{fuel}}\): Lower Heating Value (LHV) energy density reciprocal

### 2.2 Quantum-Inspired Particle Swarm Optimization (QPSO)
In classical PSO, particles follow deterministic Newtonian velocity trajectories. In **QPSO**, particles behave like quantum particles bound in a 1D Delta-potential well centered at the local attractor \(p_{ij}\):

1. **Mean Best Position (\(mbest\))**:
\[
mbest(t) = \frac{1}{M} \sum_{i=1}^{M} P_i(t)
\]

2. **Local Attractor (\(p_{ij}\))**:
\[
p_{ij}(t) = \phi \cdot P_{ij}(t) + (1 - \phi) \cdot G_j(t), \quad \phi \sim U(0, 1)
\]

3. **Quantum Position Update via Wave Function Inversion**:
\[
X_{ij}(t+1) = p_{ij}(t) \pm \alpha \cdot |mbest_j(t) - X_{ij}(t)| \cdot \ln\left(\frac{1}{u}\right), \quad u \sim U(0, 1)
\]
Where \(\alpha\) is the Contraction-Expansion coefficient annealing linearly from \(1.0 \to 0.5\).

---

## 3. Multi-Objective Pareto Fitness Function

The QPSO optimizer minimizes a normalized composite scalar objective:
\[
\min F(X) = w_1 \cdot \frac{C_{\text{fuel}}(X)}{C_0} + w_2 \cdot \frac{C_{\text{tax}}(X)}{T_0} + w_3 \cdot \frac{E_{\text{CO2}}(X)}{E_0} + w_4 \cdot \frac{T_{\text{voyage}}(X)}{H_0} - w_5 \cdot \text{Profit}(X)
\]
Subject to:
- Cargo Weight \(\le\) Vessel Max Capacity
- Operating Speed \(V_{\min} \le V \le V_{\max}\)
- Port Draft & Berth Compatibility Constraints
