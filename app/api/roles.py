from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.security import ROLE_ADMIN, get_current_user, require_roles



from app.models import (
    Rol
)
from app.schemas.schemas import RolCreate, RolOut
from typing import List

router = APIRouter(dependencies=[Depends(get_current_user)])



# ── ROL ──────────────────────────────────────────────────────
@router.get("/roles", response_model=List[RolOut], tags=["Roles"])
def listar_roles(db: Session = Depends(get_db)):
    return db.query(Rol).all()

@router.post(
    "/roles",
    response_model=RolOut,
    tags=["Roles"],
    dependencies=[Depends(require_roles(ROLE_ADMIN))],
)
def crear_rol(rol: RolCreate, db: Session = Depends(get_db)):
    obj = Rol(**rol.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.delete(
    "/roles/{idrol}",
    tags=["Roles"],
    dependencies=[Depends(require_roles(ROLE_ADMIN))],
)
def eliminar_rol(idrol: int, db: Session = Depends(get_db)):
    obj = db.query(Rol).filter(Rol.idrol == idrol).first()
    if not obj: raise HTTPException(404, "Rol no encontrado")
    db.delete(obj); db.commit()
    return {"mensaje": "Rol eliminado"}

