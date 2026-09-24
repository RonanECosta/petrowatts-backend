import base64
from flask import jsonify
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag
from model import CarroEletrico, Session, Acessorio, AcessorioCarroEletrico
from schemas.carro_eletrico import (
    VeiculoEletricoAcessoriosQuerySchema, CarroEletricoAcessoriosViewSchema
)
from schemas import ErrorSchema
from logger import logger

veiculo_eletrico_tag = Tag(name="Veículos Elétricos - EV", description="Consultas de veículos elétricos novos")
bp_veiculo_ev = APIBlueprint('veiculos-eletricos', __name__, abp_tags=[veiculo_eletrico_tag])

@bp_veiculo_ev.get('/veiculos-eletricos', tags=[veiculo_eletrico_tag])
def get_todos_veiculos_eletricos():
    """Busca todos os carros elétricos."""
    logger.debug("Coletando lista de carros elétricos")
    session = Session()
    try:
        carros = session.query(CarroEletrico).all()
        
        lista_veiculos = []
        for c in carros:
            thumbnail_base64 = None
            if c.thumbnail is not None:
                if isinstance(c.thumbnail, bytes):
                    thumbnail_base64 = base64.b64encode(c.thumbnail).decode('utf-8')
                else:
                    thumbnail_base64 = str(c.thumbnail)
                    
            lista_veiculos.append({
                "id": c.id,
                "id_fabricante": c.fabricante_ref.id if c.fabricante_ref else None,
                "modelo": c.modelo,
                "fabricante": c.fabricante_ref.fabricante if c.fabricante_ref else "Desconhecido",
                "valor_compra": c.valor_compra,
                "consumo_mj_km": c.consumo_mj_km,
                "potencia_cv": c.potencia_cv,
                "autonomia_km": c.autonomia_km,
                "capacidade_bat_kwh": c.capacidade_bat_kwh,
                "porta_malas_litros": c.porta_malas_litros,
                "necessario_infra": c.necessario_infra,
                "thumbnail": thumbnail_base64
            })
            
        return jsonify({"veiculos": lista_veiculos}), 200
        
    except Exception as e:
        logger.error(f"Erro ao listar veículos elétricos: {e}")
        return jsonify({"message": "Erro ao coletar dados do banco"}), 500
    finally:
        session.close()

@bp_veiculo_ev.get('/veiculo-eletrico-acessorios', tags=[veiculo_eletrico_tag], responses={"200": CarroEletricoAcessoriosViewSchema, "404": ErrorSchema, "500": ErrorSchema})
def get_veiculo_eletrico_acessorios(query: VeiculoEletricoAcessoriosQuerySchema):
    """Busca todos os acessórios de um veículo elétrico."""
    logger.debug(f"Coletando acessórios do veículo elétrico ID: {query.id_veiculo}")
    session = Session()
    try:
        # Consulta realizando os JOINs adequados através da tabela associativa (acessorio_carro_eletrico)
        resultados = session.query(Acessorio, AcessorioCarroEletrico)\
            .join(AcessorioCarroEletrico, Acessorio.id == AcessorioCarroEletrico.id_acessorio)\
            .join(CarroEletrico, CarroEletrico.id == AcessorioCarroEletrico.id_carro_eletrico)\
            .filter(CarroEletrico.id == query.id_veiculo)\
            .all()
        
        lista_acessorios = []
        for acessorio, ac_pivot in resultados:
            lista_acessorios.append({
                "id": acessorio.id,
                "id_veiculo": query.id_veiculo,
                "nome": acessorio.nome,
                # 'valor_tamanho' é a métrica armazenada na tabela pivot (ex: 10.25 para polegadas, 6 para airbags)
                "valor_tamanho": float(ac_pivot.valor_tamanho)
            })
            
        return jsonify({"acessorios": lista_acessorios}), 200
        
    except Exception as e:
        logger.error(f"Erro ao listar acessórios do veículo elétrico: {e}")
        return jsonify({"message": "Erro ao coletar dados do banco"}), 500
    finally:
        session.close()
