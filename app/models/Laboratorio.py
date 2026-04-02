
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey,BigInteger

from sqlalchemy.orm import relationship
from app.database.connection import Base


class Laboratorio(Base):
    __tablename__ = "LABORATORIO"
    id_laboratorio = Column(BigInteger, primary_key=True, index=True)
    nombre         = Column(String(255), nullable=False)

    productos = relationship("Producto", back_populates="laboratorio")
