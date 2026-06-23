from pydantic import BaseModel, Field
from typing import List
from decimal import Decimal
from model.carro_combustao import CarroCombustao 

class CarroCombustaoSchema(BaseModel):
    """ Define como um novo carro a combustão deve ser representado para inserção (POST).
    """
    id_fabricante: int = Field(..., description="ID do fabricante cadastrado")
    modelo: str = Field(..., max_length=50, examples=["Civic"]) 
    valor_revenda: float = Field(..., gt=0, examples=[85000.00])
    consumo: Decimal = Field(..., description="Consumo médio do veículo (ex: km/l)")
    ano: int = Field(..., gt=1900, examples=[2020], description="Ano de fabricação do veículo")

    class Config:
        json_schema_extra = {
            "example": {
                "id_fabricante": 1,
                "modelo": "Corolla",
                "valor_revenda": 95000.00,
                "consumo": "12.5",
                "ano": 2021
            }
        }


class CarroCombustaoViewSchema(BaseModel):
    """ Define como os dados de um carro a combustão serão retornados pela API.
    """
    id: int
    id_fabricante: int
    modelo: str
    valor_revenda: float
    consumo: Decimal
    ano: int

    class Config:
        # Permite ler o objeto do SQLAlchemy diretamente
        from_attributes = True 


class ListaCarrosCombustaoSchema(BaseModel):
    """ Define a estrutura de retorno de uma lista de carros a combustão.
    """
    carros: List[CarroCombustaoViewSchema]


def apresenta_carros_combustao(carros: List[CarroCombustao]):
    """ Transforma uma lista de objetos do SQLAlchemy em uma estrutura
        de dicionário compatível com o ListaCarrosCombustaoSchema.
    """
    result = []
    for carro in carros:
        result.append({
            "id": carro.id,
            "id_fabricante": carro.id_fabricante,
            "modelo": carro.modelo,
            "valor_revenda": carro.valor_revenda,
            "consumo": carro.consumo,
            "ano": carro.ano if carro.ano is not None else None,
        })

    return {"carros": result}
