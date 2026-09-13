import os
import uvicorn
from app.main import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    host = os.getenv("HOST", "0.0.0.0")
    print(f">>> QuantumFleet Master Unified Server starting on http://localhost:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")
