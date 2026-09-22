import base64
from flask import jsonify
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag
from sqlalchemy import exists
from model import CarroEletrico, Fabricante, Session
from schemas.carro_combustao import (
    AnosQuerySchema, ListagemAnosSchema, ListagemModelosSchema, 
    ModeloQueryByIdFabricanteSchema
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
