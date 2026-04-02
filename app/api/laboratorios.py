from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.security import ROLE_ADMIN, get_current_user, require_roles
from app.models import   Laboratorio

from app.schemas.schemas import   LaboratorioCreate, LaboratorioOut

from typing import List

router = APIRouter(dependencies=[Depends(get_current_user)])




# ── LABORATORIO ───────────────────────────────────────────────
@router.get("/laboratorios", response_model=List[LaboratorioOut], tags=["Catálogos"])
def listar_laboratorios(db: Session = Depends(get_db)):
    return db.query(Laboratorio).all()

@router.post(
    "/laboratorios",
    response_model=LaboratorioOut,
    tags=["Catálogos"],
    dependencies=[Depends(require_roles(ROLE_ADMIN))],
)
def crear_laboratorio(lab: LaboratorioCreate, db: Session = Depends(get_db)):
    obj = Laboratorio(**lab.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.delete(
    "/laboratorios/{id}",
    tags=["Catálogos"],
    dependencies=[Depends(require_roles(ROLE_ADMIN))],
)
def eliminar_laboratorio(id: int, db: Session = Depends(get_db)):
    obj = db.query(Laboratorio).filter(Laboratorio.id_laboratorio == id).first()
    if not obj: raise HTTPException(404, "Laboratorio no encontrado")
    db.delete(obj); db.commit()
    return {"mensaje": "Laboratorio eliminado"}
