from flask import Flask, request, send_from_directory, redirect, jsonify
from flask_openapi3.openapi import OpenAPI
from flask_openapi3.models.info import Info
from flask_openapi3.models.tag import Tag
from sqlalchemy.exc import IntegrityError
from sqlalchemy import exists
from flask_cors import CORS
from model import Usuario, Fabricante, CarroEletrico, CarroCombustao, UsuarioCarro, Session
from schemas import UsuarioSchema, UsuarioViewSchema, ErrorSchema
from logger import logger

info = Info(title="Minha API - Economia de Veículos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
usuario_tag = Tag(name="Usuário", description="Adição, visualização e remoção de usuários à base")
veiculo_eletrico_tag = Tag(name="Veículos Elétricos", description="Consultas de marcas, modelos e anos da base")
veiculo_combustao_tag = Tag(name="Veículos a Combustão", description="Consultas de marcas, modelos e anos da base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/x-icon')


@app.get('/veiculo-combustao', tags=[veiculo_combustao_tag])
def get_todos_veiculos_combustao():
    """Busca todos os carros a combustão da base para renderizar na tabela do frontend."""
    logger.debug("Coletando lista de carros a combustão da base técnica")
    session = Session()
    try:
        carros = session.query(CarroCombustao).all()
        
        lista_veiculos = []
        for c in carros:
            fabricante = c.fabricante_ref
            nome_fabricante = fabricante.fabricante if fabricante else "Desconhecido"
            
            ano_numerico = c.ano if c.ano is not None else 0
            lista_veiculos.append({
                "nome": f"{nome_fabricante} {c.modelo}",
                "quantidade": f"Ano {ano_numerico}",
                "valor": f"R$ {c.valor_revenda:,.2f}"
            })
            
        return jsonify({"veiculos": lista_veiculos}), 200
        
    except Exception as e:
        logger.error(f"Erro ao listar veículos a combustão: {e}")
        return {"message": "Erro ao coletar dados do banco"}, 500
    finally:
        session.close()

@app.get('/fabricantes', tags=[veiculo_combustao_tag])
def get_fabricantes():
    """Busca todos os fabricantes cadastrados no banco para o primeiro combo box."""
    logger.debug("Coletando lista de fabricantes")
    session = Session()
    try:
        fabricantes = session.query(Fabricante).order_by(Fabricante.fabricante).all()
        resultado = [{"id": f.id, "fabricante": f.fabricante} for f in fabricantes]
        return jsonify(resultado), 200
    except Exception as e:
        logger.error(f"Erro ao buscar fabricantes: {e}")
        return {"message": "Erro ao coletar fabricantes"}, 500
    finally:
        session.close()


@app.get('/modelos', tags=[veiculo_combustao_tag])
def get_modelos():
    """Busca os modelos de veículos filtrados pelo ID do fabricante selecionado."""
    id_fabricante = request.args.get('id_fabricante')
    logger.debug(f"Coletando modelos para o fabricante ID: {id_fabricante}")
    
    if not id_fabricante:
        return jsonify({"message": "O parâmetro id_fabricante é obrigatório"}), 400
        
    session = Session()
    try:
        modelos = session.query(CarroCombustao.modelo)\
                         .filter(CarroCombustao.id_fabricante == id_fabricante)\
                         .distinct()\
                         .order_by(CarroCombustao.modelo).all()
        resultado = [{"modelo": m[0]} for m in modelos]
        return jsonify(resultado), 200
    except Exception as e:
        logger.error(f"Erro ao buscar modelos: {e}")
        return jsonify({"message": "Erro ao coletar modelos"}), 500
    finally:
        session.close()


@app.get('/anos', tags=[veiculo_combustao_tag])
def get_anos():
    """Busca os anos disponíveis filtrados pelo nome do modelo selecionado."""
    modelo_selecionado = request.args.get('modelo')
    logger.debug(f"Coletando anos para o modelo: {modelo_selecionado}")
    
    if not modelo_selecionado:
        return {"message": "O parâmetro modelo é obrigatório"}, 400
        
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
        return {"message": "Erro ao coletar anos"}, 500
    finally:
        session.close()

@app.post('/usuario', tags=[usuario_tag], responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_usuario(form: UsuarioSchema):
    """Adiciona um novo usuário à base de dados."""
    usuario = Usuario(
        nome=form.nome,
        estado=form.estado
    )
    logger.debug(f"Adicionando usuário de nome: '{usuario.nome}'")
    try:
        session = Session()
        session.add(usuario)
        session.commit()
        logger.debug(f"Adicionado usuário de nome: '{usuario.nome}'")
        
        return {"id": usuario.id, "nome": usuario.nome, "estado": usuario.estado}, 200

    except IntegrityError as e:
        error_msg = "Usuário de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar usuário '{usuario.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar novo usuário :/"
        logger.warning(f"Erro ao adicionar usuário '{usuario.nome}', {error_msg}")
        return {"message": error_msg}, 400
    
@app.delete('/usuario', tags=[usuario_tag])
def delete_usuario():
    """Exclui um usuário da base de dados pelo CPF informado."""
    id_usuario = request.args.get('id_usuario')
    
    if not id_usuario:
        return {"message": "O parâmetro 'id_usuario' é obrigatório."}, 400

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


@app.post('/usuario-carro', tags=[usuario_tag])
def add_usuario_veiculo():
    """
    Cadastra o usuário, localiza o carro selecionado pelos combos
    e vincula ambos na tabela associativa salvando a rodagem mensal.
    """
    nome_usuario = request.form.get('nome')
    estado_usuario = request.form.get('uf')
    cpf_usuario = request.form.get('cpf')
    id_fabricante = request.form.get('id_fabricante')
    modelo_carro = request.form.get('modelo')
    ano_carro = request.form.get('ano')
    km_mensal = request.form.get('km_mensal')

    logger.debug(f"Iniciando cadastro completo para o usuário: '{nome_usuario}'")
    
    session = Session()
    try:
        carro = session.query(CarroCombustao).filter(
            CarroCombustao.id_fabricante == id_fabricante,
            CarroCombustao.modelo == modelo_carro,
            CarroCombustao.ano == ano_carro
        ).first()

        logger.info(f"Carro encontrado: {carro.modelo} ({carro.ano}) do fabricante ID {carro.id_fabricante}") if carro else logger.warning("Carro não encontrado para a combinação selecionada.")

        if not carro:
            return {"message": "A combinação de veículo selecionada não foi encontrada no banco de dados."}, 404

        novo_usuario = Usuario(cpf=cpf_usuario, nome=nome_usuario, estado=estado_usuario)
        session.add(novo_usuario)
        session.flush() # O flush gera o ID do usuário sem fechar a transação do banco
        logger.info(f"Usuário criado: {novo_usuario.nome} ({novo_usuario.cpf}) do estado {novo_usuario.estado}")

        vinculo = UsuarioCarro(
            id_usuario=novo_usuario.id,
            id_carro_combustao=carro.id,
            km_mensal = int(km_mensal) if km_mensal else 0
        )
        session.add(vinculo)
        
        session.commit()
        
        logger.debug(f"Sucesso! Usuário {novo_usuario.id} vinculado ao carro {carro.id}")
        return {
            "message": "Usuário e veículo vinculados com sucesso!",
            "id_usuario": novo_usuario.id
            }, 200

    except IntegrityError as e:
        session.rollback()
        error_msg = "Usuário com este mesmo CPF já está salvo na base."
        logger.warning(f"Erro de integridade para '{cpf_usuario}': {error_msg}")
        return {"message": error_msg}, 409
    except Exception as e:
        session.rollback()
        logger.error(f"Erro inesperado no cadastro: {e}")
        return {"message": "Não foi possível salvar o registro devido a um erro interno."}, 500
    finally:
        session.close()

@app.get('/usuario-carro', tags=[usuario_tag])
def get_usuario_veiculo():
    """
    Busca os detalhes do usuário e do veículo vinculado a ele pelo cpf.
    """
    cpf_usuario = request.args.get('cpf')
    
    if not cpf_usuario:
        return {"message": "O parâmetro 'cpf' é obrigatório."}, 400

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
                "fabricante": carro.fabricante_ref.fabricante if carro.fabricante_ref else "Desconhecido",
                "modelo": carro.modelo,
                "ano": carro.ano,
                "km_mensal": vinculo.km_mensal
            }
        }, 200

    except Exception as e:
        logger.error(f"Erro ao buscar dados do usuário: {e}")
        return {"message": "Erro interno ao buscar os dados."}, 500
    finally:
        session.close()


@app.get('/fabricantes_combustao', tags=[veiculo_combustao_tag])
def get_fabricantes_combustao():
    """Retorna fabricantes de carros `a combustão, ou sejam, que possuem pelo menos um carro a combustão cadastrado."""
    logger.debug("Coletando lista de fabricantes com carros cadastrados")
    session = Session()
    try:
        fabricantesCombustao = session.query(Fabricante).filter(exists().where(CarroCombustao.id_fabricante == Fabricante.id)).order_by(Fabricante.fabricante).all()
        
        resultado = [{"id": f.id, "fabricante": f.fabricante} for f in fabricantesCombustao]
        return jsonify(resultado), 200
        
    except Exception as e:
        logger.error(f"Erro ao buscar fabricantes de carros à combustão: {e}")
        return {"message": "Erro ao coletar dados do banco"}, 500
    finally:
        session.close()

@app.patch('/usuario-carro', tags=[usuario_tag])
def update_usuario_veiculo():
    """
    Atualiza os dados do usuário e do veículo vinculado a ele pelo cpf.
    """
    id_usuario = request.form.get('id_usuario')
    nome_usuario = request.form.get('nome')
    estado_usuario = request.form.get('uf')
    cpf_usuario = request.form.get('cpf')
    id_fabricante = request.form.get('id_fabricante')
    modelo_carro = request.form.get('modelo')
    ano_carro = request.form.get('ano')
    km_mensal = request.form.get('km_mensal')

    logger.debug(f"Iniciando alteração para o usuário: '{nome_usuario}'")
    
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