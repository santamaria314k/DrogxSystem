from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.security import (
    ROLE_ADMIN,
    ROLE_FARMACEUTICO,
    get_current_user,
    require_roles,
)
from app.models import  Inventario

from app.schemas.schemas import InventarioCreate, InventarioOut
 
from typing import List

router = APIRouter(dependencies=[Depends(get_current_user)])






# ── INVENTARIO ────────────────────────────────────────────────
@router.get("/inventario", response_model=List[InventarioOut], tags=["Inventario"])
def listar_inventario(db: Session = Depends(get_db)):
    return db.query(Inventario).all()

@router.get("/inventario/producto/{id_producto}", response_model=List[InventarioOut], tags=["Inventario"])
def inventario_por_producto(id_producto: int, db: Session = Depends(get_db)):
    return db.query(Inventario).filter(Inventario.id_producto == id_producto).all()

@router.post(
    "/inventario",
    response_model=InventarioOut,
    tags=["Inventario"],
    dependencies=[Depends(require_roles(ROLE_ADMIN, ROLE_FARMACEUTICO))],
)
def crear_inventario(inv: InventarioCreate, db: Session = Depends(get_db)):
    obj = Inventario(**inv.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.delete(
    "/inventario/{id}",
    tags=["Inventario"],
    dependencies=[Depends(require_roles(ROLE_ADMIN, ROLE_FARMACEUTICO))],
)
def eliminar_inventario(id: int, db: Session = Depends(get_db)):
    obj = db.query(Inventario).filter(Inventario.id_inventario == id).first()
    if not obj: raise HTTPException(404, "Registro de inventario no encontrado")
    db.delete(obj); db.commit()
    return {"mensaje": "Registro eliminado"}
