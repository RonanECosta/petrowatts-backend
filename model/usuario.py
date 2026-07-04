from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import relationship

from model import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String(11), nullable=False, unique=True)
    nome = Column(String(255), nullable=False)
    estado = Column(String(2), nullable=False)

    carros = relationship("UsuarioCarro", back_populates="usuario_ref", cascade="all, delete-orphan")
