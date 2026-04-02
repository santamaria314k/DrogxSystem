
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.security import (
    ROLE_ADMIN,
    get_current_user,
    get_password_hash,
    require_roles,
)

from app.models import  Usuario
from app.schemas.schemas import  UsuarioCreate, UsuarioOut

from typing import List

router = APIRouter(dependencies=[Depends(get_current_user)])



# ── USUARIO ───────────────────────────────────────────────────
@router.get(
    "/usuarios",
    response_model=List[UsuarioOut],
    tags=["Usuarios"],
    dependencies=[Depends(require_roles(ROLE_ADMIN))],
)
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.get(
    "/usuarios/{id}",
    response_model=UsuarioOut,
    tags=["Usuarios"],
    dependencies=[Depends(require_roles(ROLE_ADMIN))],
)
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    obj = db.query(Usuario).filter(Usuario.idusuario == id).first()
    if not obj: raise HTTPException(404, "Usuario no encontrado")
    return obj

@router.post(
    "/usuarios",
    response_model=UsuarioOut,
    tags=["Usuarios"],
    dependencies=[Depends(require_roles(ROLE_ADMIN))],
)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    payload = usuario.model_dump()
    payload["password"] = get_password_hash(payload["password"])
    obj = Usuario(**payload)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.delete(
    "/usuarios/{id}",
    tags=["Usuarios"],
    dependencies=[Depends(require_roles(ROLE_ADMIN))],
)
def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    obj = db.query(Usuario).filter(Usuario.idusuario == id).first()
    if not obj: raise HTTPException(404, "Usuario no encontrado")
    db.delete(obj); db.commit()
    return {"mensaje": "Usuario eliminado"}

