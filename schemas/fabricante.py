from pydantic import BaseModel, Field
from typing import List

# Importação opcional do modelo para tipagem da função auxiliar
from model.fabricante import Fabricante


class FabricanteSchema(BaseModel):
    """ Define como um novo fabricante deve ser representado para inserção (POST).
    """
    fabricante: str = Field(..., max_length=63, examples=["Toyota"])

    class Config:
        json_schema_extra = {
            "example": {
                "fabricante": "Chevrolet"
            }
        }


class FabricanteViewSchema(BaseModel):
    """ Define como os dados de um fabricante serão retornados pela API.
    """
    id: int
    fabricante: str

    class Config:
        # Permite que o Pydantic mapeie o objeto do SQLAlchemy diretamente
        from_attributes = True

class ListaFabricantesSchema(BaseModel):
    """ Define a estrutura de retorno de uma lista de fabricantes.
    """
    fabricantes: List[FabricanteViewSchema]


def apresenta_fabricantes(fabricantes: List[Fabricante]):
    """ Transforma uma lista de objetos do SQLAlchemy em uma estrutura
        de dicionário compatível com o ListaFabricantesSchema.
    """
    result = []
    for f in fabricantes:
        f: Fabricante  # Dica de tipo para evitar erros do Pylance
        
        result.append({
            "id": f.id,
            "fabricante": f.fabricante,
        })

    return {"fabricantes": result}