from pydantic import BaseModel
from typing import Optional, List
from model.usuario import Usuario


class UsuarioSchema(BaseModel):
    """ Define como um novo usuário a ser inserido deve ser representado
    """
    cpf: str = "12345678900"
    nome: str = "João"
    estado: str = "RJ"

class UsuarioViewSchema(BaseModel):
    """ Define como um usuário será retornado.
    """
    id: int = 1
    cpf: str = "12345678900"
    nome: str = "João"
    estado: str = "RJ"

def apresenta_usuarios(usuarios: List[Usuario]):
    """ Retorna uma representação do usuário seguindo o schema definido em
        UsuarioViewSchema.
    """
    result = []
    for usuario in usuarios:
        result.append({
            "id": usuario.id,
            "cpf": usuario.cpf,
            "nome": usuario.nome,
            "estado": usuario.estado,
        })

    return {"usuarios": result}