
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.security import ROLE_ADMIN, get_current_user, require_roles
from app.models import  Vigencia
from app.schemas.schemas import VigenciaCreate, VigenciaOut

from typing import List

router = APIRouter(dependencies=[Depends(get_current_user)])



# ── VIGENCIA ──────────────────────────────────────────────────
@router.get("/vigencias", response_model=List[VigenciaOut], tags=["Catálogos"])
def listar_vigencias(db: Session = Depends(get_db)):
    return db.query(Vigencia).all()

@router.post(
    "/vigencias",
    response_model=VigenciaOut,
    tags=["Catálogos"],
    dependencies=[Depends(require_roles(ROLE_ADMIN))],
)
def crear_vigencia(vigencia: VigenciaCreate, db: Session = Depends(get_db)):
    obj = Vigencia(**vigencia.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj
