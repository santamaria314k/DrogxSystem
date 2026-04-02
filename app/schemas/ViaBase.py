from pydantic import BaseModel


# ── VIA ADMINISTRACION ────────────────────────────────────────
class ViaBase(BaseModel):
    descripcion_via: str

class ViaCreate(ViaBase):
    id_via: int

class ViaOut(ViaCreate):
    class Config:
        from_attributes = True
