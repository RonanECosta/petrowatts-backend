from flask import jsonify
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag
from sqlalchemy.exc import IntegrityError
from model import Usuario, CarroCombustao, UsuarioCarro, Session
from schemas.usuario import (
    CadastroUsuarioCarroFormSchema, CadastroUsuarioCarroSucessoSchema, 
    UsuarioCarroDetalhesViewSchema, UsuarioCarroQuerySchema, UsuarioDeleteSucessoSchema,
    AtualizarUsuarioCarroFormSchema, UsuarioDeleteQuerySchema, AtualizarUsuarioCarroSucessoSchema
)
from model import Usuario, Fabricante, CarroCombustao, UsuarioCarro, Session
from schemas import ErrorSchema
from logger import logger

# Cria um blueprint específico para usuários com suas tags e prefixo de rota se quiser
usuario_tag = Tag(name="Usuário", description="Rotas de gerenciamento de usuários")
bp_usuario = APIBlueprint('usuario', __name__, abp_tags=[usuario_tag])

@bp_usuario.post('/usuario-carro', tags=[usuario_tag], responses={"200": CadastroUsuarioCarroSucessoSchema, "404": ErrorSchema, "409": ErrorSchema, "500": ErrorSchema})
def add_usuario_veiculo(form: CadastroUsuarioCarroFormSchema):
    """
    Cadastra o usuário, localiza o carro selecionado pelos combos
    e vincula ambos na tabela associativa salvando a rodagem mensal.
    """
    # Os dados agora são extraídos de forma limpa e tipada a partir do objeto 'form'
    nome_usuario = form.nome
    estado_usuario = form.uf
    cpf_usuario = form.cpf
    id_fabricante = form.id_fabricante
    modelo_carro = form.modelo
    ano_carro = form.ano
    km_mensal = form.km_mensal

    logger.debug(f"Iniciando cadastro completo para o usuário: '{nome_usuario}'")
    
    session = Session()
    try:
        carro = session.query(CarroCombustao).filter(
            CarroCombustao.id_fabricante == id_fabricante,
            CarroCombustao.modelo == modelo_carro,
            CarroCombustao.ano == ano_carro
        ).first()

        if not carro:
            return jsonify({"message": "A combinação de veículo selecionada não foi encontrada no banco de dados."}), 404

        novo_usuario = Usuario(cpf=cpf_usuario, nome=nome_usuario, estado=estado_usuario)
        session.add(novo_usuario)
        session.flush() 
        logger.info(f"Usuário criado: {novo_usuario.nome} ({novo_usuario.cpf}) do estado {novo_usuario.estado}")

        vinculo = UsuarioCarro(
            id_usuario=novo_usuario.id,
            id_carro_combustao=carro.id,
            km_mensal = km_mensal # O Pydantic já garante que chega como inteiro
        )
        session.add(vinculo)
        session.commit()
        
        logger.debug(f"Sucesso! Usuário {novo_usuario.id} vinculado ao carro {carro.id}")
        
        return jsonify({
            "message": "Usuário e veículo vinculados com sucesso!",
            "id_usuario": novo_usuario.id
        }), 200

    except IntegrityError as e:
        session.rollback()
        error_msg = "Usuário com este mesmo CPF já está salvo na base."
        logger.warning(f"Erro de integridade para '{cpf_usuario}': {error_msg}")
        return jsonify({"message": error_msg}), 409
    except Exception as e:
        session.rollback()
        logger.error(f"Erro inesperado no cadastro: {e}")
        return jsonify({"message": "Não foi possível salvar o registro devido a um erro interno."}), 500
    finally:
        session.close()

@bp_usuario.get('/usuario-carro', tags=[usuario_tag], responses={"200": UsuarioCarroDetalhesViewSchema, "404": ErrorSchema, "500": ErrorSchema})
def get_usuario_veiculo(query: UsuarioCarroQuerySchema):
    """
    Busca os detalhes do usuário e do veículo vinculado a ele pelo cpf.
    """
    cpf_usuario = query.cpf
    logger.debug(f"Buscando dados para o usuário: '{cpf_usuario}'")
    
    session = Session()
    try:
        resultado_query = session.query(Usuario, UsuarioCarro, CarroCombustao)\
            .join(UsuarioCarro, Usuario.id == UsuarioCarro.id_usuario)\
            .join(CarroCombustao, UsuarioCarro.id_carro_combustao == CarroCombustao.id)\
            .join(Fabricante, CarroCombustao.id_fabricante == Fabricante.id)\
            .filter(Usuario.cpf == cpf_usuario)\
            .first()

        if not resultado_query:
            return {"message": "Usuário ou vínculo não encontrado."}, 404

        usuario, vinculo, carro = resultado_query
        
        return {
            "id_usuario": usuario.id,
            "cpf": usuario.cpf,
            "nome": usuario.nome,
            "estado": usuario.estado,
            "veiculo": {
                "id_fabricante": carro.fabricante_ref.id if carro.fabricante_ref else "Desconhecido",
                "fabricante": carro.fabricante_ref.fabricante if carro.fabricante_ref else "Desconhecido",
                "modelo": carro.modelo,
                "ano": carro.ano,
                "km_mensal": vinculo.km_mensal
            }
        }, 200

    except Exception as e:
        logger.error(f"Erro ao buscar dados do usuário: {e}")
        return jsonify({"message": "Erro interno ao buscar os dados."}), 500
    finally:
        session.close()

@bp_usuario.patch('/usuario-carro', tags=[usuario_tag], responses={"200": AtualizarUsuarioCarroSucessoSchema, "404": ErrorSchema, "500": ErrorSchema})
def update_usuario_veiculo(form: AtualizarUsuarioCarroFormSchema):
    """
    Atualiza os dados do usuário e do veículo vinculado a ele pelo id_usuario.
    """
    # Coleta todas as variáveis diretamente do formulário validado pelo Pydantic
    id_usuario = form.id_usuario
    nome_usuario = form.nome
    estado_usuario = form.uf
    cpf_usuario = form.cpf
    id_fabricante = form.id_fabricante
    modelo_carro = form.modelo
    ano_carro = form.ano
    km_mensal = form.km_mensal

    logger.debug(f"Iniciando alteração para o usuário ID: '{id_usuario}'")
    
    session = Session()

    if not id_usuario:
        return {"message": "O parâmetro 'id_usuario' é obrigatório."}, 400

    try:
        usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
        if not usuario:
            return {"message": "Usuário não encontrado."}, 404
        
        if nome_usuario: setattr(usuario, 'nome', nome_usuario)
        if estado_usuario: setattr(usuario, 'estado', estado_usuario)
        if cpf_usuario: setattr(usuario, 'cpf', cpf_usuario)
        
        vinculo = session.query(UsuarioCarro).filter(UsuarioCarro.id_usuario == usuario.id).first()
        if not vinculo:
            return {"message": "Vínculo de veículo não encontrado."}, 404
            
        if id_fabricante and modelo_carro and ano_carro:
            carro = session.query(CarroCombustao).filter(
                CarroCombustao.id_fabricante == id_fabricante,
                CarroCombustao.modelo == modelo_carro,
                CarroCombustao.ano == ano_carro
            ).first()
            
            if carro:
                vinculo.id_carro_combustao = carro.id
            else:
                return {"message": "Novo veículo selecionado não encontrado."}, 404

        if km_mensal is not None: setattr(vinculo, 'km_mensal', int(km_mensal))
        
        session.commit()
        return {"message": "Dados atualizados com sucesso."}, 200

    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao atualizar usuário ID {id_usuario}: {e}")
        return {"message": "Erro interno ao tentar atualizar."}, 500
    finally:
        session.close()

@bp_usuario.delete('/usuario', tags=[usuario_tag], responses={"200": UsuarioDeleteSucessoSchema, "404": ErrorSchema, "500": ErrorSchema})
def delete_usuario(query: UsuarioDeleteQuerySchema):
    """Exclui um usuário da base de dados pelo ID informado na URL."""
    # O parâmetro agora é capturado via query string (?id_usuario=...) de forma tratada como inteiro
    id_usuario = query.id_usuario

    logger.debug(f"Solicitação de exclusão para o usuário com ID: '{id_usuario}'")
    
    
    session = Session()
    try:
        usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
        
        if not usuario:
            logger.warning(f"Usuário com ID '{id_usuario}' não encontrado para exclusão.")
            return {"message": "Usuário não encontrado."}, 404
        
        session.delete(usuario)
        session.commit()
        
        logger.info(f"Usuário com ID '{id_usuario}' excluído com sucesso.")
        return {"message": "Usuário excluído com sucesso."}, 200

    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao excluir usuário com ID '{id_usuario}': {e}")
        return {"message": "Erro interno ao tentar excluir o usuário."}, 500
    finally:
        session.close()