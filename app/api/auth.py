from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import Rol, Usuario
from app.security import (
    ROLE_ADMIN,
    authenticate_user,
    create_access_token,
    get_password_hash,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o password incorrecto",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"sub": user.username, "role": user.rol})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "idusuario": user.idusuario,
            "username": user.username,
            "rol": user.rol,
        },
    }


@router.post("/bootstrap-admin")
def bootstrap_admin(db: Session = Depends(get_db)):
    if db.query(Usuario).count() > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bootstrap bloqueado: ya existen usuarios",
        )

    admin_role = db.query(Rol).filter(Rol.idrol == ROLE_ADMIN).first()
    if not admin_role:
        admin_role = Rol(idrol=ROLE_ADMIN, nombrerol="Administrador")
        db.add(admin_role)

    admin_user = Usuario(
        idusuario=1,
        username="admin",
        password=get_password_hash("admin123"),
        rol=ROLE_ADMIN,
    )
    db.add(admin_user)
    db.commit()

    return {
        "message": "Usuario admin creado",
        "credentials": {"username": "admin", "password": "admin123"},
    }
