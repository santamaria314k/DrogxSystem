from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.security import ROLE_ADMIN, get_current_user, require_roles

from app.models import ViaAdministracion
from app.schemas.schemas import  ViaCreate, ViaOut

from typing import List

router = APIRouter(dependencies=[Depends(get_current_user)])


# ── VIA ADMINISTRACION ────────────────────────────────────────
@router.get("/vias", response_model=List[ViaOut], tags=["Catálogos"])
def listar_vias(db: Session = Depends(get_db)):
    return db.query(ViaAdministracion).all()

@router.post(
    "/vias",
    response_model=ViaOut,
    tags=["Catálogos"],
    dependencies=[Depends(require_roles(ROLE_ADMIN))],
)
def crear_via(via: ViaCreate, db: Session = Depends(get_db)):
    obj = ViaAdministracion(**via.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj
