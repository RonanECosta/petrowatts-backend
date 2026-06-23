from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import relationship

from model import Base


class UsuarioCarro(Base):
    __tablename__ = "usuarios_carros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_carro_combustao = Column(Integer, ForeignKey("carros_combustao.id"), nullable=False)
    km_mensal = Column(Integer, nullable=False)

    usuario_ref = relationship("Usuario", back_populates="carros")
    carro_ref = relationship("CarroCombustao", back_populates="usuarios")
