from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from model.carro_eletrico import CarroEletrico

class CarroEletricoSchema(BaseModel):
    """ Define como um novo carro elétrico a ser inserido deve ser representado.
        O campo 'thumbnail' pode ser enviado como string Base64 ou nulo.
    """
    id_fabricante: int = Field(..., description="ID do fabricante associado")
    modelo: str = Field(..., description="Modelo do veículo elétrico")
    valor_compra: float = Field(..., gt=0, description="Valor de compra do veículo")
    consumo_mj_km: Decimal = Field(..., description="Consumo em MJ/km")
    potencia_cv: int = Field(..., gt=0, description="Potência em Cavalos (CV)")
    autonomia_km: float = Field(..., gt=0, description="Autonomia total em km")
    capacidade_bat_kwh: float = Field(..., gt=0, description="Capacidade da bateria em kWh")
    porta_malas_litros: int = Field(..., gt=0, description="Capacidade do porta-malas em litros")
    necessario_infra: bool = Field(default=False, description="Indica se necessita de infraestrutura de carregamento")
    thumbnail: Optional[str] = Field(None, description="Imagem em formato Base64 ou URL")

    class Config:
        json_schema_extra = {
            "example": {
                "id_fabricante": 1,
                "modelo": "Modelo X",
                "valor_compra": 150000.00,
                "consumo_mj_km": "0.65",
                "potencia_cv": 204,
                "autonomia_km": 400.5,
                "capacidade_bat_kwh": 60.0,
                "porta_malas_litros": 400,
                "necessario_infra": True,
                "thumbnail": "data:image/png;base64,..."
            }
        }

class CarroEletricoViewSchema(BaseModel):
    """ Define como os dados de um carro elétrico serão retornados pela API.
    """
    id: int
    id_fabricante: int
    modelo: str
    valor_compra: float
    consumo_mj_km: Decimal
    potencia_cv: int
    autonomia_km: float
    capacidade_bat_kwh: float
    porta_malas_litros: int
    necessario_infra: bool
    thumbnail: Optional[str] = None
    # Habilita o Pydantic a ler o objeto do SQLAlchemy diretamente (ex: CarroEletricoViewSchema.model_validate(carro_objeto))
    class Config:
        from_attributes = True 

class ListaCarrosEletricosSchema(BaseModel):
    """ Define como uma lista de carros elétricos será retornada.
    """
    carros: List[CarroEletricoViewSchema]


def apresenta_carros(carros: List[CarroEletrico]):
    """ Função auxiliar para transformar a lista de objetos do SQLAlchemy
        em uma estrutura de dicionário compatível com o ListaCarrosEletricosSchema.
    """
    result = []
    for carro in carros:
        result.append({
            "id": carro.id,
            "id_fabricante": carro.id_fabricante,
            "modelo": carro.modelo,
            "valor_compra": carro.valor_compra,
            "consumo_mj_km": carro.consumo_mj_km,
            "potencia_cv": carro.potencia_cv,
            "autonomia_km": carro.autonomia_km,
            "capacidade_bat_kwh": carro.capacidade_bat_kwh,
            "porta_malas_litros": carro.porta_malas_litros,
            "necessario_infra": carro.necessario_infra,
            "thumbnail": carro.thumbnail,
        })

    return {"carros": result}

class CarroEletricoAcessoriosViewSchema(BaseModel):
    """ Define como os dados de um acessório de carro elétrico serão retornados pela API.
    """
    id: int
    id_veiculo: int
    nome: str
    descricao: str

    class Config:
        from_attributes = True

class VeiculoEletricoAcessoriosQuerySchema(BaseModel):
    """ Define como será feita a consulta de acessórios de um veículo elétrico.
    """
    id_veiculo: int

    class Config:
        from_attributes = True