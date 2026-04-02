from pydantic import BaseModel



# ── USUARIO ───────────────────────────────────────────────────
class UsuarioBase(BaseModel):
    username: str
    rol: int

class UsuarioCreate(UsuarioBase):
    idusuario: int
    password: str

class UsuarioOut(BaseModel):
    idusuario: int
    username:  str
    rol:       int
    class Config:
        from_attributes = True

