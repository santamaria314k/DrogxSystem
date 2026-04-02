from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ── VENTA ─────────────────────────────────────────────────────
class VentaBase(BaseModel):
    id_producto:      int
    precio_unitario:  float
    cantidad_vendida: int
    fecha_venta:      Optional[datetime] = None

class VentaCreate(VentaBase):
    id_venta: int

class VentaOut(VentaCreate):
    class Config:
        from_attributes = True
