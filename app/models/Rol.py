from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey,BigInteger

from sqlalchemy.orm import relationship
from app.database.connection import Base




class Rol(Base):
    __tablename__ = "ROL"
    idrol     = Column(BigInteger, primary_key=True, index=True)
    nombrerol = Column(String(255), nullable=False)
    usuarios  = relationship("Usuario", back_populates="rol_obj")
