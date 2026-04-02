from pydantic import BaseModel



# ── UNIDAD MEDIDA ─────────────────────────────────────────────
class UnidadBase(BaseModel):
    descripcion_unidad: str

class UnidadCreate(UnidadBase):
    id_unidad: int

class UnidadOut(UnidadCreate):
    class Config:
        from_attributes = True
