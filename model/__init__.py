import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Importação dos modelos da aplicação
from model.base import Base
from model.usuario import Usuario
from model.fabricante import Fabricante
from model.carro_combustao import CarroCombustao
from model.carro_eletrico import CarroEletrico
from model.usuario_carro import UsuarioCarro
from model.acessorio import Acessorio
from model.acessorio_carro_eletrico import AcessorioCarroEletrico

db_url = os.getenv('DATABASE_URL')

if not db_url:
    raise RuntimeError("A variável de ambiente 'DATABASE_URL' não foi configurada!")

# echo=True faz o SQLAlchemy exibir todas as queries executadas nos logs da API
engine = create_engine(db_url, echo=True)
Session = sessionmaker(bind=engine)

# Tenta conectar ao MySQL com até 10 tentativas (com espera de 3 segundos entre elas)
max_retries = 10
for attempt in range(1, max_retries + 1):
    try:
        print(f"Tentando conectar ao banco de dados (tentativa {attempt}/{max_retries})...")
        Base.metadata.create_all(engine)
        print("Conexão estabelecida com sucesso!")
        break
    except OperationalError as e:
        if attempt == max_retries:
            raise e
        print("Banco de dados ainda não está pronto. Aguardando 3 segundos...")
        time.sleep(3)