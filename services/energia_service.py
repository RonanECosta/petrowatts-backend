import requests
from logger import logger

# ID do recurso no Portal de Dados Abertos da ANEEL (Tarifas Homologadas)
RESOURCE_ID_ANEEL = "f5fe4872-9141-4e11-8270-426d0128b04d"
URL_CKAN_ANEEL = "https://dadosabertos.aneel.gov.br/api/3/action/datastore_search"


def consultar_preco_kwh_externo(uf: str) -> float:
    """
    Consulta a API CKAN da ANEEL para obter a tarifa de energia residencial (B1) por UF.
    """
    params = {
        "resource_id": RESOURCE_ID_ANEEL,
        "limit": 5,
        "q": f'{{"SigUF": "{uf.upper()}", "DscSubGrupo": "B1"}}'
    }
    
    try:
        response = requests.get(URL_CKAN_ANEEL, params=params, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            if dados.get("success"):
                records = dados.get("result", {}).get("records", [])
                if records:
                    registro = records[0]
                    # Busca os campos de valor de tarifa do registro
                    preco = registro.get("VlrTfProdutora") or registro.get("VlrTE") or 0.85
                    
                    if isinstance(preco, str):
                        preco = preco.replace(",", ".")
                        
                    return float(preco)
            logger.warning(f"Nenhum registro encontrado na ANEEL para UF '{uf}'. Usando valor padrão (0.85).")
        else:
            logger.warning(f"API ANEEL retornou status {response.status_code}. Usando valor padrão (0.85).")
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de conexão ao consultar ANEEL: {e}. Usando valor padrão (0.85).")
        
    return 0.85  # Fallback padrão de segurança


def calcular_custo_energia(km_mensal: float, consumo_kwh_por_km: float, uf: str) -> dict:
    """
    Calcula o custo total estimado de eletricidade para uma determinada quilometragem e estado.
    
    Parâmetros:
        - km_mensal: Distância percorrida em km.
        - consumo_kwh_por_km: Eficiência do veículo elétrico (kWh/km).
        - uf: Sigla do estado brasileiro (ex: 'RJ', 'SP', 'MG').
        
    Retorna um dicionário com o detalhamento dos custos.
    """
    try:
        # Validações básicas de entrada
        if km_mensal < 0 or consumo_kwh_por_km < 0:
            raise ValueError("Quilometragem e consumo por km devem ser valores positivos.")
            
        if not uf or len(uf) != 2:
            raise ValueError("UF inválida. Forneça a sigla do estado com 2 letras (ex: 'SP').")

        # 1. Busca o preço do kWh no estado informado
        preco_kwh = consultar_preco_kwh_externo(uf)
        
        # 2. Realiza os cálculos de consumo
        total_kwh = km_mensal * consumo_kwh_por_km
        custo_total = total_kwh * preco_kwh
        
        logger.debug(
            f"Cálculo concluído | UF: {uf.upper()} | {km_mensal} km * {consumo_kwh_por_km} kWh/km "
            f"= {total_kwh:.2f} kWh -> R$ {custo_total:.2f} (Tarifa: R$ {preco_kwh}/kWh)"
        )

        return {
            "uf": uf.upper(),
            "km_mensal": float(km_mensal),
            "consumo_kwh_por_km": float(consumo_kwh_por_km),
            "total_kwh_consumido": round(total_kwh, 2),
            "tarifa_kwh_aplicada": round(preco_kwh, 4),
            "custo_total_rs": round(custo_total, 2)
        }

    except ValueError as ve:
        logger.warning(f"Erro de validação em calcular_custo_energia: {ve}")
        raise ve
    except Exception as e:
        logger.error(f"Erro inesperado ao calcular custo de energia: {e}")
        raise ValueError("Erro interno ao processar o cálculo do custo de energia.")