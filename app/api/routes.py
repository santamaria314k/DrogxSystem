from fastapi import APIRouter

from .auth import router as auth_router
from .inventario import router as inventario_router
from .laboratorios import router as laboratorios_router
from .productos import router as productos_router
from .roles import router as roles_router
from .unidades import router as unidades_router
from .usuarios import router as usuarios_router
from .ventas import router as ventas_router
from .vias import router as vias_router
from .vigencias import router as vigencias_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(productos_router)
router.include_router(inventario_router)
router.include_router(ventas_router)
router.include_router(roles_router)
router.include_router(unidades_router)
router.include_router(vias_router)
router.include_router(vigencias_router)
router.include_router(laboratorios_router)
router.include_router(usuarios_router)
