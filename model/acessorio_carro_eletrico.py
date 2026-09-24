from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Float
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import relationship

from model import Base


class AcessorioCarroEletrico(Base):
    __tablename__ = "acessorio_carro_eletrico"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_carro_eletrico = Column(Integer, ForeignKey('carros_eletricos.id'), nullable=False)
    id_acessorio = Column(Integer, ForeignKey('acessorios.id'), nullable=False)
    valor_tamanho = Column(Float, nullable=False)

    carro_eletrico_ref = relationship("CarroEletrico", back_populates="acessorios")
    acessorio_ref = relationship("Acessorio", back_populates="carros")