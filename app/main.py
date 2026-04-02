import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from .db.connection import Base, engine 
from app.api.routes import router
import app.models.models

app = FastAPI(
    title="API — Sistema de Gestión de medicamentos",
    description="CRUD completo sobre MySQL para productos, inventario, ventas y catálogos.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluimos las rutas
app.include_router(router, prefix="/api/v1")


@app.on_event("startup")
def startup_db_init():
    for _ in range(30):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            Base.metadata.create_all(bind=engine)
            return
        except Exception:
            time.sleep(2)

    raise RuntimeError("No se pudo conectar a MySQL durante el arranque")

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "docs": "/docs"}