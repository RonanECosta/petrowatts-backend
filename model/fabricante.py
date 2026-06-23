from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import relationship

from model import Base


class Fabricante(Base):
    __tablename__ = "fabricantes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fabricante = Column(String(63), nullable=False)

    carros_eletricos = relationship("CarroEletrico", back_populates="fabricante_ref")
    carros_combustao = relationship("CarroCombustao", back_populates="fabricante_ref")
