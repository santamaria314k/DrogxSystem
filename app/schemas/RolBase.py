
from pydantic import BaseModel






# ── ROL ──────────────────────────────────────────────────────
class RolBase(BaseModel):
    nombrerol: str

class RolCreate(RolBase):
    idrol: int

class RolOut(RolCreate):
    class Config:
        from_attributes = True

