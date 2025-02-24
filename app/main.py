from fastapi import FastAPI, HTTPException
import random
import logging
import json
from datetime import datetime, timezone
from prometheus_fastapi_instrumentator import Instrumentator

# Configurar logging con formato estructurado en JSON
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("service-b")

def log_json(level, component, message, status_code=None):
    log_entry = {
        "level": level,
        "time": datetime.now(timezone.utc).isoformat(),
        "component": component,
        "message": message
    }
    if status_code is not None:
        log_entry["status_code"] = status_code
    print(json.dumps(log_entry))

app = FastAPI()

# Instrumentar Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def maybe_fail():
    if random.random() < 0.5:  # Falla el 50% de las veces
        log_json("error", "service-b", "Service B failed with internal error.", 500)
        raise HTTPException(status_code=500, detail="Internal Server Error in Service B")

    log_json("info", "service-b", "Service B responded successfully.", 200)
    return {"message": "Hello from Service B"}

@app.get("/health")
async def health_check():
    log_json("info", "service-b", "Health check endpoint called.", 200)
    return {"status": "ok", "service": "B"}
