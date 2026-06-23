from flask import Flask, request, send_from_directory, redirect, jsonify
from flask_openapi3.openapi import OpenAPI
from flask_openapi3.models.info import Info
from flask_openapi3.models.tag import Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS

# Importe os novos modelos de Fabricante e CarroEletrico do seu pacote model
from model import Usuario, Fabricante, CarroEletrico, CarroCombustao, UsuarioCarro, Session
from schemas import UsuarioSchema, UsuarioViewSchema, ErrorSchema
from logger import logger

info = Info(title="Minha API - Economia de Veículos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definição das tags para a documentação Swagger
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
        # Busca os carros cadastrados
        carros = session.query(CarroCombustao).all()
        
        lista_veiculos = []
        for c in carros:
            # Acessa o relacionamento para obter o nome do fabricante
            fabricante = c.fabricante_ref
            nome_fabricante = fabricante.fabricante if fabricante else "Desconhecido"
            
            ano_numerico = c.ano if c.ano is not None else 0
            lista_veiculos.append({
                "nome": f"{nome_fabricante} {c.modelo}", # Ex: "Fiat Uno"
                "quantidade": f"Ano {ano_numerico}",        # Ex: "Ano 2015"
                "valor": f"R$ {c.valor_revenda:,.2f}"     # Ex: "R$ 35,000.00"
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
        # Busca todos os fabricantes ordenados por nome
        fabricantes = session.query(Fabricante).order_by(Fabricante.fabricante).all()
        
        # Converte o resultado para o formato JSON que o JS espera: [{id: 1, fabricante: 'Tesla'}, ...]
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
        # CORREÇÃO: Alinhado o order_by para usar CarroCombustao.modelo
        modelos = session.query(CarroCombustao.modelo)\
                         .filter(CarroCombustao.id_fabricante == id_fabricante)\
                         .distinct()\
                         .order_by(CarroCombustao.modelo).all()
        
        # Como o .query(CarroCombustao.modelo) retorna uma lista de tuplas de um elemento, 
        # acessamos a posição [0] de cada linha para pegar a string pura do modelo
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
        # Busca os anos cadastrados para aquele modelo específico
        anos = session.query(CarroCombustao.ano)\
                      .filter(CarroCombustao.modelo == modelo_selecionado)\
                      .distinct()\
                      .order_by(CarroCombustao.ano.desc()).all()
        
        # Retorna no formato esperado pelo JS: [{ano: 2023}, {ano: 2024}]
        resultado = [{"ano": int(float(a.ano))} for a in anos]
        return jsonify(resultado), 200
    except Exception as e:
        logger.error(f"Erro ao buscar anos: {e}")
        return {"message": "Erro ao coletar anos"}, 500
    finally:
        session.close()

@app.post('/usuario', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
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
        
        # IMPORTANTE: Para evitar o erro de lazy loading do SQLAlchemy fora da sessão,
        # convertemos o retorno para um dicionário antes de responder, se necessário.
        return {"nome": usuario.nome, "estado": usuario.estado}, 200

    except IntegrityError as e:
        error_msg = "Usuário de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar usuário '{usuario.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar novo usuário :/"
        logger.warning(f"Erro ao adicionar usuário '{usuario.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.post('/usuario-veiculo', tags=[usuario_tag])
def add_usuario_veiculo():
    """
    Cadastra o usuário, localiza o carro selecionado pelos combos
    e vincula ambos na tabela associativa salvando a rodagem mensal.
    """
    # Captura os dados enviados via FormData ou JSON do JavaScript
    # Usando request.form para manter compatibilidade com o FormData original do seu JS
    nome_usuario = request.form.get('nome')
    estado_usuario = request.form.get('estado')
    id_fabricante = request.form.get('id_fabricante')
    modelo_carro = request.form.get('modelo')
    ano_carro = request.form.get('ano')
    km_mensal = request.form.get('km_mensal')

    logger.debug(f"Iniciando cadastro completo para o usuário: '{nome_usuario}'")
    
    session = Session()
    try:
        # 1. Encontra o ID do Carro correspondente à combinação selecionada nos combos
        carro = session.query(CarroCombustao).filter(
            CarroCombustao.id_fabricante == id_fabricante,
            CarroCombustao.modelo == modelo_carro,
            CarroCombustao.ano == ano_carro
        ).first()

        if not carro:
            return {"message": "A combinação de veículo selecionada não foi encontrada no banco de dados."}, 404

        # 2. Cria e adiciona o Usuário
        novo_usuario = Usuario(nome=nome_usuario, estado=estado_usuario)
        session.add(novo_usuario)
        session.flush() # O flush gera o ID do usuário sem fechar a transação do banco

        # 3. Cria o vínculo na tabela associativa 'usuario_carro'
        vinculo = UsuarioCarro(
            id_usuario=novo_usuario.id,
            id_carro_combustao=carro.id,
            km_mensal = int(km_mensal) if km_mensal else 0
        )
        session.add(vinculo)
        
        # Efetiva todas as operações juntas no banco de dados
        session.commit()
        
        logger.debug(f"Sucesso! Usuário {novo_usuario.id} vinculado ao carro {carro.id}")
        return {"message": "Usuário e veículo vinculados com sucesso!"}, 200

    except IntegrityError as e:
        session.rollback()
        error_msg = "Usuário com este mesmo nome já está salvo na base."
        logger.warning(f"Erro de integridade para '{nome_usuario}': {error_msg}")
        return {"message": error_msg}, 409
    except Exception as e:
        session.rollback()
        logger.error(f"Erro inesperado no cadastro: {e}")
        return {"message": "Não foi possível salvar o registro devido a um erro interno."}, 500
    finally:
        session.close()
