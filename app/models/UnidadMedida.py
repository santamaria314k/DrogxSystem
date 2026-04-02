from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey,BigInteger

from sqlalchemy.orm import relationship
from app.database.connection import Base



class UnidadMedida(Base):
    __tablename__ = "UNIDADMEDIDA"
    id_unidad          = Column(BigInteger, primary_key=True, index=True)
    descripcion_unidad = Column(String(255), nullable=False)

    productos = relationship("Producto", back_populates="unidad")
