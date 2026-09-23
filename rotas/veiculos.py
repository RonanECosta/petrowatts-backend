from flask import jsonify
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag
from sqlalchemy import exists
from model import CarroCombustao, Fabricante, Session
from schemas.carro_combustao import (
    AnosQuerySchema, ListagemAnosSchema, ListagemModelosSchema, 
    ModeloQueryByIdFabricanteSchema
)
from schemas import ErrorSchema
from logger import logger

veiculo_combustao_tag = Tag(name="Veículos a Combustão", description="Consultas de marcas, modelos e anos da base")
bp_veiculo = APIBlueprint('veiculo', __name__, abp_tags=[veiculo_combustao_tag])

@bp_veiculo.get('/veiculo-combustao', tags=[veiculo_combustao_tag])
def get_todos_veiculos_combustao():
    """Busca todos os carros a combustão."""
    logger.debug("Coletando lista de carros a combustão")
    session = Session()
    try:
        carros = session.query(CarroCombustao).all()
        
        lista_veiculos = []
        for c in carros:
            lista_veiculos.append({
                "id": c.id,
                "id_fabricante": c.fabricante_ref.id if c.fabricante_ref else None,
                "fabricante": c.fabricante_ref.fabricante if c.fabricante_ref else "Desconhecido",
                "modelo": c.modelo,
                "valor_revenda": f"{c.valor_revenda:.2f}",
                "ano": f"{c.ano:.0f}",
                "consumo": f"{c.consumo:.2f} km/l"
            })
            
        return jsonify({"veiculos": lista_veiculos}), 200
        
    except Exception as e:
        logger.error(f"Erro ao listar veículos a combustão: {e}")
        return {"message": "Erro ao coletar dados do banco"}, 500
    finally:
        session.close()


@bp_veiculo.get('/modelos', tags=[veiculo_combustao_tag], responses={"200": ListagemModelosSchema, "500": ErrorSchema})
def get_modelos(query: ModeloQueryByIdFabricanteSchema):
    """Busca os modelos de veículos filtrados pelo ID do fabricante selecionado."""
    # Acessa a propriedade id_fabricante definida no seu ModeloQueryByIdFabricanteSchema
    id_fabricante = query.id_fabricante
    logger.debug(f"Coletando modelos para o fabricante ID: {id_fabricante}")
        
    session = Session()
    try:
        modelos = session.query(CarroCombustao.id, CarroCombustao.modelo)\
                         .filter(CarroCombustao.id_fabricante == id_fabricante)\
                         .distinct()\
                         .order_by(CarroCombustao.modelo).all()
        resultado = [{"id": m[0], "modelo": m[1]} for m in modelos]
        return jsonify(resultado), 200
    except Exception as e:
        logger.error(f"Erro ao buscar modelos: {e}")
        return jsonify({"message": "Erro ao coletar modelos"}), 500
    finally:
        session.close()


@bp_veiculo.get('/anos', tags=[veiculo_combustao_tag], responses={"200": ListagemAnosSchema, "500": ErrorSchema})
def get_anos(query: AnosQuerySchema):
    """Busca os anos disponíveis filtrados pelo nome do modelo selecionado."""
    # O parâmetro agora é extraído do objeto query validado
    modelo_selecionado = query.modelo
    logger.debug(f"Coletando anos para o modelo: {modelo_selecionado}")
    
    session = Session()
    try:
        anos = session.query(CarroCombustao.ano)\
                      .filter(CarroCombustao.modelo == modelo_selecionado)\
                      .distinct()\
                      .order_by(CarroCombustao.ano.desc()).all()
        
        resultado = [{"ano": int(float(a.ano))} for a in anos]
        return jsonify(resultado), 200
    except Exception as e:
        logger.error(f"Erro ao buscar anos: {e}")
        return jsonify({"message": "Erro ao coletar anos"}), 500
    finally:
        session.close()

@bp_veiculo.get('/fabricantes_combustao', tags=[veiculo_combustao_tag])
def get_fabricantes_combustao():
    """Retorna fabricantes de carros `a combustão, ou sejam, que possuem pelo menos um carro a combustão cadastrado."""
    logger.debug("Coletando lista de fabricantes com carros cadastrados")
    session = Session()
    try:
        fabricantes_combustao = session.query(Fabricante).filter(exists().where(CarroCombustao.id_fabricante == Fabricante.id)).order_by(Fabricante.fabricante).all()
        
        resultado = [{"id": f.id, "fabricante": f.fabricante} for f in fabricantes_combustao]
        return jsonify(resultado), 200
        
    except Exception as e:
        logger.error(f"Erro ao buscar fabricantes de carros à combustão: {e}")
        return {"message": "Erro ao coletar dados do banco"}, 500
    finally:
        session.close()