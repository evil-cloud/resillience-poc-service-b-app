from fastapi import FastAPI, HTTPException
import random
import logging
from prometheus_fastapi_instrumentator import Instrumentator

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Instrumentar Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def maybe_fail():
    if random.random() < 0.5:  # Falla el 50% de las veces
        logger.error("Service B falló!")
        raise HTTPException(status_code=500, detail="Error en Service B")

    logger.info("Service B respondió exitosamente")
    return {"message": "Hola desde B"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "B"}

