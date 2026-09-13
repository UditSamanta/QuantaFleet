import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .config import settings
from .database import engine, Base, SessionLocal
from .seed.seed_data import seed_database
from .routes.auth_routes import router as auth_router
from .routes.port_routes import router as port_router
from .routes.vessel_routes import router as vessel_router
from .routes.ml_routes import router as ml_router
from .routes.emission_routes import router as emission_router
from .routes.recommend_routes import router as recommend_router
from .routes.dashboard_routes import router as dashboard_router

# Ensure tables and seed data exist at import time
Base.metadata.create_all(bind=engine)
_db = SessionLocal()
try:
    seed_database(_db)
finally:
    _db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title="QuantumFleet Unified Platform",
    description="Quantum-Inspired Fuel Consumption Prediction and Green Fleet Optimization System (SIH26138)",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers under /api
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(port_router, prefix=settings.API_V1_STR)
app.include_router(vessel_router, prefix=settings.API_V1_STR)
app.include_router(ml_router, prefix=settings.API_V1_STR)
app.include_router(emission_router, prefix=settings.API_V1_STR)
app.include_router(recommend_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "system": "QuantumFleet SIH26138 Master Unified Engine",
        "modules": [
            "Unified React Single-Page Application",
            "PostgreSQL/SQLite Maritime Database",
            "ML Fuel Prediction (XGBoost/RF/Linear)",
            "IMO Emission & Carbon Tax Engine",
            "Quantum-Inspired Optimizer (QPSO)",
            "Optimizer Benchmark Suite (QPSO/PSO/SA/NSGA-II)",
            "AI Operational Insights Engine"
        ]
    }

# -------------------------------------------------------------
# UNIFIED FRONTEND SERVING (COMBINE FRONTEND & BACKEND ON ONE URL)
# -------------------------------------------------------------
possible_dist_paths = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")),
    os.path.abspath("frontend/dist"),
    os.path.abspath("../frontend/dist"),
    "D:/Desktop/quntum fleat/omganesh/frontend/dist",
]

frontend_dist = None
for p in possible_dist_paths:
    if os.path.exists(p) and os.path.exists(os.path.join(p, "index.html")):
        frontend_dist = p
        break

if frontend_dist:
    assets_path = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/") or full_path == "api" or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            return None
        target_file = os.path.join(frontend_dist, full_path)
        if os.path.exists(target_file) and os.path.isfile(target_file):
            return FileResponse(target_file)
        return FileResponse(os.path.join(frontend_dist, "index.html"))
