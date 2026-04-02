from pydantic import BaseModel
from typing import Optional
from datetime import datetime




# ── PRODUCTO ──────────────────────────────────────────────────
class ProductoBase(BaseModel):
    nombre_producto: str
    cantidad:        int
    id_unidad:       int
    id_via:          int
    expediente:      Optional[int]       = None
    fechaexpedicion: Optional[datetime]  = None
    id_vigencia:     int
    id_laboratorio:  int

class ProductoCreate(ProductoBase):
    id_producto: int

class ProductoOut(ProductoCreate):
    class Config:
        from_attributes = True
