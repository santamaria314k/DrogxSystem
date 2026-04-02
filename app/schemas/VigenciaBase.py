from pydantic import BaseModel




# ── VIGENCIA ──────────────────────────────────────────────────
class VigenciaBase(BaseModel):
    descripcion_vigencia: str

class VigenciaCreate(VigenciaBase):
    id_vigencia: int

class VigenciaOut(VigenciaCreate):
    class Config:
        from_attributes = True
