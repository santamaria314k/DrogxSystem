from pydantic import BaseModel





# ── LABORATORIO ───────────────────────────────────────────────
class LaboratorioBase(BaseModel):
    nombre: str

class LaboratorioCreate(LaboratorioBase):
    id_laboratorio: int

class LaboratorioOut(LaboratorioCreate):
    class Config:
        from_attributes = True

