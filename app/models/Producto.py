from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey,BigInteger

from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.database.connection import Base





class Producto(Base):
    __tablename__ = "PRODUCTO"
    id_producto     = Column(BigInteger, primary_key=True, index=True)
    nombre_producto = Column(String(255), nullable=False)
    cantidad        = Column(Integer, nullable=False, default=0)
    id_unidad       = Column(BigInteger, ForeignKey("UNIDADMEDIDA.id_unidad"),    nullable=False)
    id_via          = Column(BigInteger, ForeignKey("VIAADMINISTRACION.id_via"),  nullable=False)
    expediente      = Column(Integer)
    fechaexpedicion = Column(DateTime)
    id_vigencia     = Column(BigInteger, ForeignKey("VIGENCIA.id_vigencia"),      nullable=False)
    id_laboratorio  = Column(BigInteger, ForeignKey("LABORATORIO.id_laboratorio"),nullable=False)

    unidad      = relationship("UnidadMedida",    back_populates="productos")
    via         = relationship("ViaAdministracion",back_populates="productos")
    vigencia    = relationship("Vigencia",         back_populates="productos")
    laboratorio = relationship("Laboratorio",      back_populates="productos")
    inventarios = relationship("Inventario",       back_populates="producto")
    ventas      = relationship("Venta",            back_populates="producto")
