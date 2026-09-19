import requests
from logger import logger

# ID do recurso de Tarifas Homologadas no CKAN da ANEEL
RESOURCE_ID_ANEEL = "f5fe4872-9141-4e11-8270-426d0128b04d"
URL_CKAN_ANEEL = "https://dadosabertos.aneel.gov.br/api/3/action/datastore_search"

def consultar_preco_kwh_externo(uf: str) -> float:
    """
    Consulta a API do CKAN da ANEEL para obter a tarifa média residencial (kWh) por UF.
    Filtra os dados diretamente via query sem baixar arquivos pesados.
    """
    # Filtros e parâmetros da query SQL/Search do CKAN
    params = {
        "resource_id": RESOURCE_ID_ANEEL,
        "limit": 10,
        # Filtra por Estado (SigUF) e Subgrupo Residencial (B1)
        "q": f'{{"SigUF": "{uf.upper()}", "DscSubGrupo": "B1"}}'
    }
    
    try:
        # Faz a requisição GET na API da ANEEL
        response = requests.get(URL_CKAN_ANEEL, params=params, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            
            if dados.get("success"):
                records = dados.get("result", {}).get("records", [])
                
                if records:
                    # Extrai a tarifa do primeiro registro retornado
                    # Ajuste a chave conforme o campo retornado (ex: 'VlrTfProdutora' ou 'VlrTE')
                    primeiro_registro = records[0]
                    preco = primeiro_registro.get("VlrTfProdutora") or primeiro_registro.get("VlrTE") or 0.85
                    
                    # Converte vírgula para ponto caso o valor venha formatado como string ("0,85")
                    if isinstance(preco, str):
                        preco = preco.replace(",", ".")
                        
                    return float(preco)
                
                logger.warning(f"Nenhum registro encontrado na ANEEL para UF: {uf}. Usando valor padrão.")
            else:
                logger.warning("A API da ANEEL respondeu com falha no resultado.")
                
            return 0.85  # Valor padrão como fallback
            
        else:
            logger.warning(f"API ANEEL retornou status {response.status_code}. Usando valor padrão.")
            return 0.85
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de conexão ao consultar API da ANEEL: {e}")
        return 0.85  # Fallback de segurança para a aplicação