
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey,BigInteger

from sqlalchemy.orm import relationship

from app.database.connection import Base



class Vigencia(Base):
    __tablename__ = "VIGENCIA"
    id_vigencia          = Column(BigInteger, primary_key=True, index=True)
    descripcion_vigencia = Column(String(255), nullable=False)

    productos = relationship("Producto", back_populates="vigencia")
