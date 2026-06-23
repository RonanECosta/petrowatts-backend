from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import relationship

from model import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column("Nome", String(255), nullable=True)
    estado = Column("Estado", String(2), nullable=True)

    carros = relationship("UsuarioCarro", back_populates="usuario_ref")
