# QuantumFleet: Final Technical Project Report (SIH26138)

**Smart India Hackathon 2026**  
**Team**: Vanakkam  
**Theme**: Smart Vehicles / Intelligent Transportation  
**Project Title**: Quantum-Inspired Fuel Consumption Prediction and Green Fleet Optimization System

---

# Table of Contents
1. **Chapter 1: Introduction & Problem Formulation**
2. **Chapter 2: Literature Review & Theoretical Foundations**
3. **Chapter 3: System Architecture & Data Pipeline**
4. **Chapter 4: Machine Learning Fuel Prediction Engine**
5. **Chapter 5: Quantum Particle Swarm Optimization (QPSO)**
6. **Chapter 6: Full-Stack Web Implementation & UI Design**
7. **Chapter 7: Results, Benchmarks, Business Impact & Conclusion**

---

# Chapter 1: Introduction & Problem Formulation
Maritime transportation forms the backbone of global commerce, accounting for over 80% of world trade volume. However, the international shipping sector generates over one billion metric tons of greenhouse gases annually. With the implementation of the European Union Emissions Trading System (EU ETS) maritime directive (taxing $CO_2$ emissions at \$85 per metric ton) and the International Maritime Organization (IMO) Carbon Intensity Indicator (CII) regulations, commercial fleet operators face unprecedented operational and regulatory challenges.

Current voyage planning relies heavily on legacy noon-report spreadsheets or static heuristics, leading to suboptimal vessel assignments, excessive fuel burn, and severe regulatory tax penalties. **QuantumFleet** addresses this dilemma by deploying a physics-informed gradient boosted machine learning model coupled with Quantum Particle Swarm Optimization (QPSO) to deliver clean, actionable, Pareto-optimal fleet dispatching decisions in sub-second execution times.

---

# Chapter 2: Literature Review & Theoretical Foundations
Traditional approaches to vessel speed optimization and routing fall into two categories:
1. **Empirical Power Curves**: Based purely on classical naval architecture Admiralty coefficients ($P \propto \Delta^{2/3} V^3$). While physically sound, these formulas fail to capture the stochastic non-linear dynamics of real-world ocean swell, hull fouling, and multi-fuel combustion characteristics.
2. **Classical Heuristic Solvers**: Standard Particle Swarm Optimization (PSO), Genetic Algorithms (GA), and Simulated Annealing (SA). While effective for low-dimensional problems, classical PSO particles quickly suffer from velocity stagnation, trapping the optimizer in local minima on multimodal maritime routing surfaces.

Quantum-Inspired Particle Swarm Optimization (QPSO), originally introduced by Sun et al. (2004), replaces Newtonian particle velocity vectors with a quantum wave function in a localized delta-potential well. Because the quantum probability density function exhibits infinite support, particles possess a non-zero probability of materializing beyond high-fitness barriers (quantum tunneling), ensuring robust global convergence.

---

# Chapter 3: System Architecture & Data Pipeline
The QuantumFleet system is built on a 3-tier decoupled architecture:
1. **Data Engineering Layer**: Ingests and harmonizes 7 standard maritime datasets:
   - `vessels.csv`: 105 cargo ships with multi-fuel configurations.
   - `voyages.csv`: 1,311 historical voyage telemetry logs.
   - `fuel_consumption.csv`: EU MRV verified emissions benchmarks.
   - `weather.csv`: Ocean wind speed, swell wave height, and currents.
   - `fuel_prices.csv`: Global bunker price quotes per fuel type.
   - `ports.csv`: 42 global port hubs from the World Port Index.
   - `emission_factors.csv`: IMO greenhouse gas emission factors ($CO_2$, $NO_x$, $SO_x$).
2. **Data Pipeline (ETL)**: Cleans missing values, normalizes physical units (Knots, Nautical Miles, Metric Tons, USD), resolves UN/LOCODEs, and loads structured tables into PostgreSQL/SQLite via SQLAlchemy ORM.
3. **Backend Intelligence Engine**: FastAPI microservices handling ML predictions, carbon taxation, and QPSO executions.
4. **Frontend Presentation**: React 18 single-page application with Tailwind CSS adhering to the Emerald Green maritime aesthetic.

---

# Chapter 4: Machine Learning Fuel Prediction Engine
The machine learning pipeline predicts total voyage fuel consumption based on 9 core features: Distance (NM), Cargo Weight (Tons), Average Speed (Knots), Wind Speed (Knots), Wave Height (Meters), Visibility (NM), Fuel Type, Ship Type, and Deadweight Tonnage (DWT).

### Benchmark Comparison
- **Linear Regression (Baseline)**: $R^2 = 0.6759$, $\text{RMSE} = 834.90$ Tons, $\text{MAE} = 511.19$ Tons.
- **Random Forest Regressor**: $R^2 = 0.8362$, $\text{RMSE} = 593.51$ Tons, $\text{MAE} = 222.01$ Tons.
- **XGBoost Regressor (Selected Winner)**: $R^2 = 0.8824$ (5-Fold CV $R^2 = 0.9486$), $\text{RMSE} = 502.99$ Tons, $\text{MAE} = 169.47$ Tons.

The trained XGBoost model pipeline is serialized using Joblib for real-time inference in sub-5ms latency.

---

# Chapter 5: Quantum Particle Swarm Optimization (QPSO)
The QPSO engine optimizes multi-variable decisions (vessel selection, route distance, sailing speed, and fuel type).

### Algorithmic Equations
1. **Mean Best Consensus**:
   \[
   mbest(t) = \frac{1}{M} \sum_{i=1}^M P_i(t)
   \]
2. **Local Attractor**:
   \[
   p_{ij}(t) = \phi \cdot P_{ij}(t) + (1-\phi) \cdot G_j(t), \quad \phi \sim U(0, 1)
   \]
3. **Quantum Position Inversion**:
   \[
   X_{ij}(t+1) = p_{ij}(t) \pm \alpha \cdot |mbest_j(t) - X_{ij}(t)| \cdot \ln\left(\frac{1}{u}\right), \quad u \sim U(0, 1)
   \]
Where $\alpha$ anneals from $1.0 \to 0.5$ across generations.

### Multi-Objective Fitness Evaluation
\[
\min \text{Fitness} = w_1 \cdot \frac{\text{Fuel Cost}}{C_0} + w_2 \cdot \frac{\text{Carbon Tax}}{T_0} + w_3 \cdot \frac{\text{CO}_2 \text{ Emissions}}{E_0} + w_4 \cdot \frac{\text{Travel Hours}}{H_0}
\]

---

# Chapter 6: Full-Stack Web Implementation & UI Design
The client application is divided into 6 cohesive operational modules:
1. **Executive Dashboard**: Real-time KPI summaries, monthly fuel transition trends, and voyage cost breakdowns.
2. **Voyage Planning & QPSO Optimizer**: Port search autocomplete with 1-click top-10 ranked recommendations.
3. **Fleet Management Registry**: Filterable catalog of 105 cargo vessels.
4. **Live ML Fuel Simulator**: Interactive feature adjustment sliders comparing Linear, Random Forest, and XGBoost predictions.
5. **Emission & Carbon Tax Analytics**: Detailed IMO $CO_2, NO_x, SO_x$ breakdown and EU ETS compliance analyzer.
6. **AI Insights & Metaheuristic Benchmarks**: Proactive operational speed advisories and empirical QPSO vs PSO vs NSGA-II vs SA comparison tables.

---

# Chapter 7: Results, Benchmarks, Business Impact & Conclusion
### Empirical Highlights:
- **Cost Reduction**: QPSO achieves an average of **+24.8% financial savings** over conventional voyage planning.
- **Emissions Reduction**: Green alternative fuels (Bio-Methanol, LNG, Ammonia) yield up to **-64.2% carbon reduction**.
- **Execution Performance**: Computes complete Pareto-optimal fleet configurations in under 150 milliseconds.

QuantumFleet provides a scalable, mathematically rigorous, and production-ready solution to accelerate the global maritime industry’s transition toward sustainable, zero-emission shipping.
