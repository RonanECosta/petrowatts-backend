from pydantic import BaseModel, Field
from typing import List

from model.acessorio import Acessorio

class AcessorioSchema(BaseModel):
    """ Define como um novo acessório deve ser representado para inserção (POST).
    """
    nome: str = Field(..., max_length=255, examples=["Teto Solar", "Carregador Rápido"])

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "Banco de Couro"
            }
        }


class AcessorioViewSchema(BaseModel):
    """ Define como os dados de um acessório serão retornados pela API.
    """
    id: int
    nome: str

    class Config:
        from_attributes = True


class ListaAcessoriosSchema(BaseModel):
    """ Define a estrutura de retorno de uma lista de acessórios.
    """
    acessorios: List[AcessorioViewSchema]


def apresenta_acessorios(acessorios: List[Acessorio]):
    """ Transforma uma lista de objetos do SQLAlchemy em uma estrutura
        de dicionário compatível com o ListaAcessoriosSchema.
    """
    result = []
    for a in acessorios:
        a: Acessorio
        
        result.append({
            "id": a.id,
            "nome": a.nome,
        })

    return {"acessorios": result}