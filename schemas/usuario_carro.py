from pydantic import BaseModel, Field
from typing import List

# Importação opcional do modelo para tipagem da função auxiliar
from model.usuario_carro import UsuarioCarro


class UsuarioCarroSchema(BaseModel):
    """ Define como a associação de um usuário a um carro deve ser enviada (POST).
    """
    id_usuario: int = Field(..., description="ID do usuário dono do carro")
    id_carro_combustao: int = Field(..., description="ID do carro a combustão associado")
    km_mensal: int = Field(..., gt=0, examples=[1200], description="Quilometragem média percorrida por mês")

    class Config:
        json_schema_extra = {
            "example": {
                "id_usuario": 2,
                "id_carro_combustao": 1,
                "km_mensal": 1500
            }
        }


class UsuarioCarroViewSchema(BaseModel):
    """ Define como a associação entre usuário e carro será retornada pela API.
    """
    id: int
    id_usuario: int
    id_carro_combustao: int
    km_mensal: int

    class Config:
        from_attributes = True


class ListaUsuariosCarrosSchema(BaseModel):
    """ Define a estrutura de retorno de uma lista de vínculos de usuários e carros.
    """
    vinculos: List[UsuarioCarroViewSchema]


def apresenta_vinculos_carro(vinculos: List[UsuarioCarro]):
    """ Transforma uma lista de objetos do SQLAlchemy em uma estrutura
        de dicionário compatível com o ListaUsuariosCarrosSchema.
    """
    result = []
    for v in vinculos:
        v: UsuarioCarro  # Proteção de tipagem para evitar alertas do Pylance
        
        result.append({
            "id": v.id,
            "id_usuario": v.id_usuario,
            "id_carro_combustao": v.id_carro_combustao,
            "km_mensal": v.km_mensal,
        })

    return {"vinculos": result}