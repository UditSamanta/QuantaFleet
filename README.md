# 🚢 QuantumFleet — Quantum-Inspired Fuel Consumption Prediction & Green Fleet Optimization

**QuantumFleet** is a full-stack maritime decision-support platform designed to help shipping companies and fleet operators make **fuel-efficient, cost-effective, and environmentally responsible voyage planning decisions**.

The platform combines **physics-informed machine learning, weather-aware fuel prediction, maritime hydrodynamics, carbon-emission analytics, and Quantum Particle Swarm Optimization (QPSO)** into a single system.

Instead of relying solely on traditional spreadsheets and static voyage planning, QuantumFleet uses historical and operational data to estimate fuel consumption and intelligently optimize voyage parameters such as **vessel speed, route selection, and fuel usage**.

The ultimate goal is simple:

> **Reduce fuel consumption → Reduce operating costs → Reduce carbon emissions → Improve fleet efficiency.**

---

## 🌍 Why QuantumFleet?

Maritime shipping is responsible for transporting the majority of global trade, but it also contributes significantly to global greenhouse-gas emissions.

Fuel consumption in a vessel is influenced by several interconnected factors, including:

* 🚢 Vessel characteristics and specifications
* ⚓ Vessel speed
* 🌊 Wave height and sea conditions
* 💨 Wind speed and environmental resistance
* 🗺️ Voyage distance and route
* ⛽ Fuel consumption characteristics
* 🌱 Carbon-emission requirements
* 💰 Fuel and carbon-related operational costs

Traditional fleet-management systems often depend on manually maintained noon reports, historical averages, or isolated optimization techniques. Such approaches can make it difficult to evaluate multiple voyage scenarios simultaneously.

**QuantumFleet addresses this challenge by bringing prediction and optimization together.**

The system first estimates expected fuel consumption using machine-learning models and then uses a **quantum-inspired optimization algorithm** to search for better combinations of voyage parameters.

---

# ✨ Key Features

## 🚢 1. Fleet Management

QuantumFleet provides a centralized fleet-management interface for maintaining information about multiple vessels.

Each vessel can contain important operational and technical parameters such as:

* Vessel name and identification
* Vessel type
* Length and dimensions
* Deadweight / capacity
* Engine-related information
* Fuel characteristics
* Operational speed
* Other vessel-specific parameters

The platform is designed to scale to **100+ vessels**, allowing fleet operators to manage and analyze multiple ships from a single dashboard.

---

## 🧠 2. Machine Learning-Based Fuel Prediction

At the core of QuantumFleet is a **fuel-consumption prediction engine**.

The system uses machine-learning models to estimate expected fuel consumption based on vessel and voyage characteristics.

Supported model approaches include:

* **XGBoost**
* **Random Forest**
* **Linear Regression**

The training data is generated using a **physics-informed Admiralty power-law hydrodynamic model**, providing a realistic relationship between vessel characteristics, speed, and propulsion requirements.

This approach combines:

> **Domain knowledge + Physics-based modelling + Machine Learning**

rather than treating fuel consumption as a purely statistical problem.

### Example Prediction Flow

```text
Vessel Specifications
        ↓
Voyage Parameters
        ↓
Environmental Conditions
        ↓
Physics-Informed Features
        ↓
ML Fuel Prediction Model
        ↓
Estimated Fuel Consumption
```

This allows the system to quickly evaluate different voyage scenarios before actual deployment.

---

# ⚛️ 3. Quantum Particle Swarm Optimization (QPSO)

One of the major components that differentiates QuantumFleet from conventional fleet-management systems is its **Quantum Particle Swarm Optimization (QPSO)** engine.

QPSO is a **quantum-inspired optimization technique** derived from particle swarm optimization concepts and quantum-behaviour-inspired search mechanisms.

Instead of evaluating only a single predefined voyage plan, the optimizer searches through a large solution space to identify potentially better combinations of:

* Vessel speed
* Voyage distance
* Fuel consumption
* Operational cost
* Carbon emissions

The QPSO engine uses a **delta-potential-well-inspired particle update mechanism** to improve exploration of the search space and reduce the tendency to become trapped in poor local solutions.

### Optimization Concept

```text
Possible Voyage Solutions
          ↓
    Initialize Swarm
          ↓
 Evaluate Fuel + Cost + Emissions
          ↓
 Quantum-Inspired Search
          ↓
 Update Candidate Solutions
          ↓
 Evaluate Again
          ↓
 Pareto-Optimal Solutions
```

The optimizer is designed for **sub-second execution**, enabling rapid comparison of voyage scenarios.

---

# 📊 4. Multi-Objective / Pareto Optimization

Voyage planning is rarely a single-objective problem.

For example:

* Increasing speed may reduce voyage duration but increase fuel consumption.
* Reducing speed may save fuel but increase voyage time.
* A shorter route may reduce distance but encounter unfavorable weather.
* A fuel-efficient voyage may not always be the lowest-cost option after carbon pricing.

QuantumFleet therefore approaches voyage planning as a **multi-objective optimization problem**.

The system evaluates trade-offs between objectives such as:

### ⛽ Fuel Consumption

Minimize the amount of fuel required for the voyage.

### 💰 Operational Cost

Minimize the estimated economic cost associated with fuel and carbon emissions.

### 🌱 Carbon Emissions

Minimize greenhouse-gas emissions associated with fuel consumption.

Instead of returning only one answer, the optimizer can generate a **Pareto-optimal set of solutions**, allowing fleet operators to choose a solution according to their operational priorities.

---

# 🌊 5. Weather-Aware Fuel Estimation

Real-world vessel performance is affected by environmental conditions.

QuantumFleet incorporates environmental factors such as:

* 💨 Wind speed
* 🌊 Wave height
* 🌐 Environmental resistance

These factors can influence the effective resistance experienced by a vessel and therefore its expected fuel consumption.

The platform uses these conditions to produce **drag-adjusted fuel estimates**, making predictions more representative of realistic voyage conditions than a simple distance-and-speed calculation.

---

# 🌱 6. Emission & Carbon Cost Analytics

Fuel consumption directly influences a vessel's environmental footprint.

QuantumFleet converts predicted fuel usage into estimated emissions using applicable **IMO emission factors**.

The platform can then estimate potential carbon-related costs, including **EU ETS-related projections**, helping operators understand the financial impact of emissions alongside fuel costs.

### Example Analytics Flow

```text
Predicted Fuel Consumption
          ↓
Emission Factor
          ↓
Estimated CO₂ Emissions
          ↓
Carbon Cost Estimation
          ↓
Total Voyage Cost
```

This allows fleet operators to compare voyage plans not only from a fuel perspective, but also from a **carbon and financial perspective**.

---

# 🗺️ 7. Interactive Voyage Planning

QuantumFleet includes an interactive voyage-planning interface designed to make complex optimization results easier to understand.

The system provides:

* Interactive maps
* Route visualization
* Port selection
* Port autocomplete
* Voyage distance information
* Route comparison
* Optimized voyage recommendations

The map-based interface allows users to visually understand the relationship between the selected ports and the proposed voyage route.

---

# 📈 8. Executive Fleet Dashboard

The executive dashboard provides a high-level overview of fleet performance.

It can present important KPIs such as:

* Total fleet size
* Estimated fuel consumption
* Fuel savings
* Carbon emissions
* Estimated carbon cost
* Voyage performance
* Optimization results
* Model performance
* Operational trends

This gives decision-makers a quick understanding of the fleet's current and projected performance without requiring them to inspect individual voyages manually.

---

# 🤖 9. AI-Powered Insights

QuantumFleet is designed to convert raw model and optimization outputs into **actionable insights**.

Instead of simply displaying numbers, the platform can highlight observations such as:

* Potential fuel-saving opportunities
* High-emission voyages
* Speed-related fuel trade-offs
* Cost-saving opportunities
* Better-performing voyage alternatives
* Optimization recommendations

The objective is to make technical analytics understandable and useful for fleet operators and decision-makers.

---

# 🔐 10. Secure Authentication

QuantumFleet includes JWT-based authentication to support a multi-user environment.

The authentication system provides:

* User registration/login
* JWT-based authorization
* Protected API endpoints
* Session-aware frontend interactions
* User-specific access to platform functionality

This provides a foundation for deploying the platform in a multi-user fleet-management environment.

---

# 🏗️ System Architecture

QuantumFleet follows a modern full-stack architecture that separates the user interface, backend APIs, machine-learning components, optimization engine, and database.

```text
                    ┌───────────────────────┐
                    │      React Frontend    │
                    │  Dashboard / Maps / UI │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │      FastAPI Backend   │
                    │      REST APIs / Auth  │
                    └───────────┬───────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
       ┌─────────────┐   ┌──────────────┐  ┌──────────────┐
       │ ML Engine   │   │ QPSO Engine   │  │ Analytics    │
       │ Fuel Model  │   │ Optimization  │  │ & Emissions  │
       └─────────────┘   └──────────────┘  └──────────────┘
              │                 │                 │
              └─────────────────┼─────────────────┘
                                ▼
                    ┌───────────────────────┐
                    │   SQLite / PostgreSQL │
                    │      Database         │
                    └───────────────────────┘
```

---

# 🧠 Technical Approach

QuantumFleet combines several computational techniques into a single decision-support pipeline.

### Step 1 — Vessel & Voyage Input

The user provides vessel specifications and voyage information such as:

* Vessel characteristics
* Origin and destination
* Speed
* Route parameters
* Weather conditions

### Step 2 — Feature Engineering

Relevant physical and operational features are extracted and transformed for use by the prediction models.

### Step 3 — Fuel Consumption Prediction

The machine-learning engine predicts expected fuel consumption using trained regression models.

### Step 4 — Emission Calculation

Predicted fuel consumption is converted into estimated CO₂ emissions using relevant emission factors.

### Step 5 — Cost Calculation

Fuel and carbon-related costs are estimated for the voyage.

### Step 6 — QPSO Optimization

The quantum-inspired optimizer searches through possible combinations of voyage parameters.

### Step 7 — Pareto Analysis

Candidate solutions are compared across fuel, cost, and emissions objectives.

### Step 8 — Recommendation

The system presents optimized voyage alternatives through the dashboard and interactive map.

---

# 🛠️ Technology Stack

| Layer                    | Technologies                 |
| ------------------------ | ---------------------------- |
| **Frontend**             | React 18, Vite, Tailwind CSS |
| **Maps & Visualization** | Leaflet                      |
| **Backend**              | FastAPI, Python              |
| **Database**             | SQLite / PostgreSQL          |
| **ORM**                  | SQLAlchemy                   |
| **Machine Learning**     | scikit-learn, XGBoost        |
| **Optimization**         | Custom Quantum-Inspired PSO  |
| **Authentication**       | JWT                          |
| **Deployment**           | Docker, Docker Compose       |
| **Data Processing**      | Python, NumPy, Pandas        |

---

# 📁 Project Structure

```text
Quantum-Fleet/
│
├── backend/
│   ├── api/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── ml/
│   ├── optimizer/
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── App.jsx
│
├── data/
│
├── models/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

*The exact directory structure may vary depending on the current implementation.*

---

# ⚡ Performance

QuantumFleet is designed with fast decision-making in mind.

The optimization engine is capable of generating voyage recommendations in **sub-second execution time**, making it suitable for interactive scenario analysis.

This enables users to quickly experiment with different:

* Vessel speeds
* Routes
* Weather conditions
* Fuel assumptions
* Optimization objectives

without waiting for lengthy optimization cycles.

---

# 🎯 Example Use Case

Consider a vessel travelling between two ports.

A conventional approach might simply calculate the expected fuel consumption using a fixed cruising speed.

QuantumFleet can instead evaluate multiple scenarios:

| Scenario        |  Speed |   Fuel | Emissions |   Cost |
| --------------- | -----: | -----: | --------: | -----: |
| Fast Voyage     |   High |   High |      High |   High |
| Balanced Voyage | Medium | Medium |    Medium | Medium |
| Green Voyage    |    Low |    Low |       Low |    Low |

The QPSO engine searches across the possible solution space and identifies **Pareto-efficient alternatives**.

The operator can then select a voyage plan based on the company's priority:

> **Minimum fuel / Minimum cost / Minimum emissions / Balanced operation**

---

# 🌱 Environmental Impact

QuantumFleet is built around the idea that **operational efficiency and environmental sustainability can be optimized together**.

Reducing unnecessary fuel consumption can potentially lead to:

* Lower operating costs
* Lower CO₂ emissions
* Improved carbon-intensity performance
* Better fuel efficiency
* More sustainable fleet operations

The platform therefore treats environmental performance as a core optimization objective rather than an afterthought.

---

# 🏆 Hackathon Background

QuantumFleet was originally developed for **Smart India Hackathon 2026** under:

**Problem Statement:** `SIH26138`
**Domain:** Smart Vehicles / Logistics

The project explores how **machine learning and quantum-inspired optimization techniques** can be applied to a real-world logistics problem.

The central idea was to move beyond conventional fleet monitoring and build an intelligent system capable of **predicting, optimizing, and recommending** better voyage decisions.

---

# 🚀 Future Scope

QuantumFleet can be further extended into a production-grade maritime optimization platform.

Potential future improvements include:

### 🌐 Real-Time Weather Integration

Connect the platform to live marine weather and ocean-condition APIs.

### 🛰️ AIS-Based Vessel Tracking

Integrate Automatic Identification System (AIS) data for real-time vessel monitoring.

### 📡 Real-Time Fuel Monitoring

Connect onboard sensors and IoT devices to continuously update fuel-consumption predictions.

### 🧠 Advanced ML Models

Experiment with:

* Neural Networks
* LSTM/GRU models
* Transformer-based time-series models
* Physics-Informed Neural Networks

### ⚛️ Real Quantum Computing

Extend the current quantum-inspired optimizer toward hybrid quantum-classical optimization using quantum computing frameworks.

### 🗺️ Dynamic Route Optimization

Continuously update routes based on:

* Weather
* Congestion
* Port conditions
* Fuel prices
* Vessel status

### ☁️ Cloud Deployment

Deploy the complete platform using cloud infrastructure for large-scale fleet operations.

---

# 🔬 What Makes QuantumFleet Different?

QuantumFleet is not simply a fuel prediction model or a route-planning application.

It combines multiple layers of intelligence:

```text
Physics
   +
Machine Learning
   +
Weather Awareness
   +
Emission Analytics
   +
Quantum-Inspired Optimization
   +
Interactive Decision Support
```

This combination allows the platform to move from:

**"How much fuel will this voyage consume?"**

to:

**"What voyage strategy provides the best balance between fuel, cost, emissions, and operational requirements?"**

---

# 📌 Project Highlights

* 🚢 Full-stack maritime fleet-management platform
* 🧠 Machine-learning-based fuel prediction
* ⚛️ Custom Quantum Particle Swarm Optimization engine
* 📊 Multi-objective Pareto optimization
* 🌊 Weather-aware fuel estimation
* 🌱 CO₂ emission and carbon-cost analytics
* 🗺️ Interactive voyage planning
* 📈 Executive fleet dashboard
* 🔐 JWT-based authentication
* 🐳 Docker-ready architecture
* ⚡ Sub-second optimization execution
* 🌍 Designed for sustainable maritime logistics

---

# 👨‍💻 Project Team

**QuantumFleet**
Developed as part of **Smart India Hackathon 2026**

**Problem Statement:** SIH26138 — Smart Vehicles / Logistics

---

# 📄 License

This project is developed for educational, research, and hackathon purposes.

See the repository license for detailed terms and conditions.

---

# ⭐ Support the Project

If you find **QuantumFleet** interesting or useful, consider giving the repository a ⭐ on GitHub.

Feedback, suggestions, and contributions are welcome.

---

## 🚢 QuantumFleet

> **Predict smarter. Optimize better. Sail greener.**
