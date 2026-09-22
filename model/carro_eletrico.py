from sqlalchemy.sql.sqltypes import Integer, Float, Boolean, Numeric, LargeBinary, String
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship

from model import Base


class CarroEletrico(Base):
    __tablename__ = "carros_eletricos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_fabricante = Column(Integer, ForeignKey("fabricantes.id"), nullable=False)
    modelo = Column(String(50), nullable=False)
    valor_compra = Column(Float, nullable=False)
    consumo_mj_km = Column(Numeric, nullable=False)
    potencia_cv = Column(Integer, nullable=False)
    autonomia_km = Column(Float, nullable=False)
    capacidade_bat_kwh = Column(Float, nullable=False)
    porta_malas_litros = Column(Integer, nullable=False)
    necessario_infra = Column(Boolean, nullable=False)
    thumbnail = Column(LargeBinary, nullable=True)

    fabricante_ref = relationship("Fabricante", back_populates="carros_eletricos")
    acessorios = relationship("AcessorioCarroEletrico", back_populates="carro_eletrico_ref")
