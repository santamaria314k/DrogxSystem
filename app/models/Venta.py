
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey,BigInteger

from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.database.connection import Base



class Venta(Base):
    __tablename__ = "VENTA"
    id_venta         = Column(BigInteger, primary_key=True, index=True)
    id_producto      = Column(BigInteger, ForeignKey("PRODUCTO.id_producto"), nullable=False)
    precio_unitario  = Column(Float, nullable=False)
    cantidad_vendida = Column(Integer, nullable=False)
    fecha_venta      = Column(DateTime)

    producto = relationship("Producto", back_populates="ventas")
