
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey,BigInteger

from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.database.connection import Base



class Usuario(Base):
    __tablename__ = "USUARIO"
    idusuario = Column(BigInteger, primary_key=True, index=True)
    username  = Column(String(255), nullable=False, unique=True)
    password  = Column(String(255), nullable=False)
    rol       = Column(BigInteger, ForeignKey("ROL.idrol"), nullable=False)

    rol_obj   = relationship("Rol", back_populates="usuarios")
