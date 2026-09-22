from sqlalchemy.sql.sqltypes import Integer, Float, Numeric, String
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship

from model import Base


class CarroCombustao(Base):
    __tablename__ = "carros_combustao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_fabricante = Column(Integer, ForeignKey("fabricantes.id"), nullable=False)
    modelo = Column(String(50), nullable=False)
    valor_revenda = Column(Float, nullable=False)
    consumo = Column(Numeric, nullable=False)
    ano = Column(Numeric, nullable=False)

    fabricante_ref = relationship("Fabricante", back_populates="carros_combustao")
    usuarios = relationship("UsuarioCarro", back_populates="carro_combustao_ref")
