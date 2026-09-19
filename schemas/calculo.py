from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class CalculoEnergiaQuerySchema(BaseModel):
    """ Define os parâmetros necessários para consultar o cálculo de custo 
        energético de um veículo elétrico via Query Parameters.
    """
    km_mensal: float = Field(
        1000.0, 
        gt=0, 
        description="Quilometragem percorrida no mês (em km)"
    )
    uf: str = Field(
        "RJ", 
        min_length=2, 
        max_length=2, 
        description="Sigla da Unidade Federativa (UF) do Brasil"
    )
    consumo_kwh_por_km: float = Field(
        0.15, 
        gt=0, 
        description="Eficiência/consumo médio do veículo elétrico (kWh/km)"
    )


class CalculoEnergiaViewSchema(BaseModel):
    """ Define como o resultado detalhado do cálculo de energia será retornado.
    """
    uf: str = Field("RJ", description="UF consultada")
    km_mensal: float = Field(1000.0, description="Quilometragem mensal")
    consumo_kwh_por_km: float = Field(0.15, description="Consumo aplicado em kWh por km")
    total_kwh_consumido: float = Field(150.0, description="Consumo total em kWh para a quilometragem")
    tarifa_kwh_aplicada: float = Field(0.85, description="Tarifa do kWh obtida na ANEEL (ou valor padrão)")
    custo_total_rs: float = Field(127.50, description="Custo total estimado em Reais (R$)")


def apresenta_calculo_energia(dados_calculo: Dict[str, Any]) -> Dict[str, Any]:
    """ Retorna uma representação padronizada do cálculo do custo de energia
        seguindo o schema definido em CalculoEnergiaViewSchema.
    """
    return {
        "uf": dados_calculo.get("uf", "RJ"),
        "km_mensal": dados_calculo.get("km_mensal", 0.0),
        "consumo_kwh_por_km": dados_calculo.get("consumo_kwh_por_km", 0.15),
        "total_kwh_consumido": dados_calculo.get("total_kwh_consumido", 0.0),
        "tarifa_kwh_aplicada": dados_calculo.get("tarifa_kwh_aplicada", 0.85),
        "custo_total_rs": dados_calculo.get("custo_total_rs", 0.0)
    }


class ComparativoEnergiaCombustivelQuerySchema(BaseModel):
    """ Define os parâmetros necessários para calcular e comparar o gasto
        entre veículo a combustível e elétrico.
    """
    km_mensal: float = Field(1000.0, gt=0, description="Quilometragem percorrida no mês")
    uf: str = Field("RJ", min_length=2, max_length=2, description="UF para consulta de tarifas")
    consumo_kwh_por_km: Optional[float] = Field(0.15, gt=0, description="Consumo elétrico em kWh/km")
    preco_gasolina_litro: Optional[float] = Field(5.80, gt=0, description="Preço do litro da gasolina (R$)")
    autonomia_km_por_litro: Optional[float] = Field(10.0, gt=0, description="Autonomia do carro a combustão (km/l)")


class ComparativoEnergiaViewSchema(BaseModel):
    """ Define o formato de resposta comparando os gastos entre elétrico e combustível.
    """
    uf: str = Field("RJ", description="UF consultada")
    km_mensal: float = Field(1000.0, description="Quilometragem mensal calculada")
    custo_eletrico_rs: float = Field(127.50, description="Custo mensal do veículo elétrico (R$)")
    custo_combustivel_rs: float = Field(580.00, description="Custo mensal do veículo a combustão (R$)")
    economia_mensal_rs: float = Field(452.50, description="Economia mensal estimada usando elétrico (R$)")


class ErrorSchema(BaseModel):
    """ Define como as mensagens de erro serão estruturadas em caso de falha.
    """
    message: str = "Erro ao processar a requisição de cálculo."