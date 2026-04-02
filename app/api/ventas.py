from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.security import (
    ROLE_ADMIN,
    ROLE_VENDEDOR,
    get_current_user,
    require_roles,
)

from app.models import  Producto , Venta

from app.schemas.schemas import  VentaCreate, VentaOut

from typing import List

router = APIRouter(dependencies=[Depends(get_current_user)])


# ── VENTA ─────────────────────────────────────────────────────
@router.get("/ventas", response_model=List[VentaOut], tags=["Ventas"])
def listar_ventas(db: Session = Depends(get_db)):
    return db.query(Venta).all()

@router.get("/ventas/{id}", response_model=VentaOut, tags=["Ventas"])
def obtener_venta(id: int, db: Session = Depends(get_db)):
    obj = db.query(Venta).filter(Venta.id_venta == id).first()
    if not obj: raise HTTPException(404, "Venta no encontrada")
    return obj

@router.post(
    "/ventas",
    response_model=VentaOut,
    tags=["Ventas"],
    dependencies=[Depends(require_roles(ROLE_ADMIN, ROLE_VENDEDOR))],
)
def crear_venta(venta: VentaCreate, db: Session = Depends(get_db)):
    # Verificar stock
    producto = db.query(Producto).filter(Producto.id_producto == venta.id_producto).first()
    if not producto: raise HTTPException(404, "Producto no encontrado")
    if producto.cantidad < venta.cantidad_vendida:
        raise HTTPException(400, f"Stock insuficiente. Disponible: {producto.cantidad}")
    # Descontar stock
    producto.cantidad -= venta.cantidad_vendida
    obj = Venta(**venta.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.delete(
    "/ventas/{id}",
    tags=["Ventas"],
    dependencies=[Depends(require_roles(ROLE_ADMIN, ROLE_VENDEDOR))],
)
def eliminar_venta(id: int, db: Session = Depends(get_db)):
    obj = db.query(Venta).filter(Venta.id_venta == id).first()
    if not obj: raise HTTPException(404, "Venta no encontrada")
    db.delete(obj); db.commit()
    return {"mensaje": "Venta eliminada"}
