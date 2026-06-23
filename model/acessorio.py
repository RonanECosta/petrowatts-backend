from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import relationship

from model import Base


class Acessorio(Base):
    __tablename__ = "acessorios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)

    carros = relationship("AcessorioCarroEletrico", back_populates="acessorio_ref")
