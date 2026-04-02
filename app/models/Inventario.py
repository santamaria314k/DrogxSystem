
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey,BigInteger
from sqlalchemy.orm import relationship
from app.db.connection import Base



class Inventario(Base):
    __tablename__ = "INVENTARIO"
    id_inventario = Column(BigInteger, primary_key=True, index=True)
    id_producto   = Column(BigInteger, ForeignKey("PRODUCTO.id_producto"), nullable=False)
    cantidad      = Column(Integer, nullable=False, default=0)
    fechaingreso  = Column(DateTime)

    producto = relationship("Producto", back_populates="inventarios")
