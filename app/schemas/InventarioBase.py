from pydantic import BaseModel
from typing import Optional
from datetime import datetime





# ── INVENTARIO ────────────────────────────────────────────────
class InventarioBase(BaseModel):
    id_producto:  int
    cantidad:     int
    fechaingreso: Optional[datetime] = None

class InventarioCreate(InventarioBase):
    id_inventario: int

class InventarioOut(InventarioCreate):
    class Config:
        from_attributes = True

