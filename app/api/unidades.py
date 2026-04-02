
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.security import ROLE_ADMIN, get_current_user, require_roles
from app.models import UnidadMedida

from app.schemas.schemas import (UnidadCreate, UnidadOut)

from typing import List

router = APIRouter(dependencies=[Depends(get_current_user)])



# ── UNIDAD MEDIDA ─────────────────────────────────────────────
@router.get("/unidades", response_model=List[UnidadOut], tags=["Catálogos"])
def listar_unidades(db: Session = Depends(get_db)):
    return db.query(UnidadMedida).all()

@router.post(
    "/unidades",
    response_model=UnidadOut,
    tags=["Catálogos"],
    dependencies=[Depends(require_roles(ROLE_ADMIN))],
)
def crear_unidad(unidad: UnidadCreate, db: Session = Depends(get_db)):
    obj = UnidadMedida(**unidad.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj
