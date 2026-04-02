from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey,BigInteger

from sqlalchemy.orm import relationship
from app.database.connection import Base



class ViaAdministracion(Base):
    __tablename__ = "VIAADMINISTRACION"
    id_via          = Column(BigInteger, primary_key=True, index=True)
    descripcion_via = Column(String(255), nullable=False)

    productos = relationship("Producto", back_populates="via")
