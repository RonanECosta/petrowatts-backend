from pydantic import BaseModel, Field
from typing import List

# Importação opcional do modelo para tipagem da função auxiliar
from model.acessorio_carro_eletrico import AcessorioCarroEletrico


class AcessorioCarroEletricoSchema(BaseModel):
    """ Define o vínculo de um acessório a um carro elétrico para inserção (POST).
    """
    id_carro: int = Field(..., description="ID do carro elétrico associado")
    id_acessorio: int = Field(..., description="ID do acessório associado")
    valor_tamanho: float = Field(..., gt=0, examples=[17.5], description="Valor do tamanho, dimensão ou medida do acessório")

    class Config:
        json_schema_extra = {
            "example": {
                "id_carro": 1,
                "id_acessorio": 3,
                "valor_tamanho": 17.5
            }
        }


class AcessorioCarroEletricoViewSchema(BaseModel):
    """ Define como o vínculo do acessório ao carro elétrico será retornado.
    """
    id: int
    id_carro: int
    id_acessorio: int
    valor_tamanho: float

    class Config:
        from_attributes = True


class ListaAcessoriosCarrosEletricosSchema(BaseModel):
    """ Define a estrutura de retorno de uma lista de vínculos de acessórios.
    """
    vinculos: List[AcessorioCarroEletricoViewSchema]


def apresenta_acessorios_carro(vinculos: List[AcessorioCarroEletrico]):
    """ Transforma uma lista de objetos do SQLAlchemy em uma estrutura
        de dicionário compatível com o ListaAcessoriosCarrosEletricosSchema.
    """
    result = []
    for v in vinculos:
        v: AcessorioCarroEletrico  # Evita alertas do Pylance
        
        result.append({
            "id": v.id,
            "id_carro": v.id_carro,
            "id_acessorio": v.id_acessorio,
            "valor_tamanho": v.valor_tamanho,
        })

    return {"vinculos": result}
