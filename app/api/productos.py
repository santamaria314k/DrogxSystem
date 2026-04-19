from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.security import (
    ROLE_ADMIN,
    ROLE_FARMACEUTICO,
    ROLE_VENDEDOR,
    get_current_user,
    require_roles,
)

from app.models import  Producto

from app.schemas.schemas import  ProductoCreate, ProductoOut
   
from typing import List

router = APIRouter(dependencies=[Depends(get_current_user)])


# ── PRODUCTO ──────────────────────────────────────────────────
@router.get("/productos", response_model=List[ProductoOut], tags=["Productos"])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()

@router.get("/productos/{id}", response_model=ProductoOut, tags=["Productos"])
def obtener_producto(id: int, db: Session = Depends(get_db)):
    obj = db.query(Producto).filter(Producto.id_producto == id).first()
    if not obj: raise HTTPException(404, "Producto no encontrado")
    return obj

@router.post(
    "/productos",
    response_model=ProductoOut,
    tags=["Productos"],
    dependencies=[Depends(require_roles(ROLE_ADMIN,ROLE_VENDEDOR, ROLE_FARMACEUTICO))],
)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    obj = Producto(**producto.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.put(
    "/productos/{id}",
    response_model=ProductoOut,
    tags=["Productos"],
    dependencies=[Depends(require_roles(ROLE_ADMIN))],
)
def actualizar_producto(id: int, datos: ProductoCreate, db: Session = Depends(get_db)):
    obj = db.query(Producto).filter(Producto.id_producto == id).first()
    if not obj: raise HTTPException(404, "Producto no encontrado")
    for k, v in datos.model_dump().items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete(
    "/productos/{id}",
    tags=["Productos"],
    dependencies=[Depends(require_roles(ROLE_ADMIN))],
)
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    obj = db.query(Producto).filter(Producto.id_producto == id).first()
    if not obj: raise HTTPException(404, "Producto no encontrado")
    db.delete(obj); db.commit()
    return {"mensaje": "Producto eliminado"}

