from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.engine.create import create_engine
import os

# importando os elementos definidos no modelo
from model.base import Base
from model.acessorio import Acessorio
from model.carro_combustao import CarroCombustao
from model.carro_eletrico import CarroEletrico
from model.acessorio_carro_eletrico import AcessorioCarroEletrico
from model.fabricante import Fabricante
from model.usuario import Usuario
from model.usuario_carro import UsuarioCarro


db_path = "database/"

if not os.path.exists(db_path):
   os.makedirs(db_path)

# url de acesso ao banco
db_url = 'sqlite:///%s/db.sqlite3' % db_path

engine = create_engine(db_url, echo=False)

Session = sessionmaker(bind=engine)

if not database_exists(engine.url):
    create_database(engine.url) 

Base.metadata.create_all(engine)

# carrega dados iniciais no BD
def carregar_dados_iniciais():
    """Lê os arquivos sql para popular o BD"""
    session = Session()
    try:
        if session.query(CarroEletrico).count() == 0 and session.query(CarroCombustao).count() == 0:
            caminho_sql_veic_elet = os.path.join(db_path, "carga-veiculos-eletricos.sql")
            caminho_sql_veic_comb = os.path.join(db_path, "carga-veiculos-combustao.sql")
            
            if not os.path.exists(caminho_sql_veic_elet) or not os.path.exists(caminho_sql_veic_comb):
                print(f"Arquivo(s) de carga não foram encontrados na pasta '{db_path}'.")
                return

            print("Populando banco de dados com os arquivos SQL...")
            
            with open(caminho_sql_veic_elet, "r", encoding="utf-8") as f_elet:
                sql_eletricos = f_elet.read()

            with open(caminho_sql_veic_comb, "r", encoding="utf-8") as f_comb:
                sql_combustao = f_comb.read()

            # Executa os scripts sequencialmente dentro da mesma transação da engine
            with engine.connect() as connection:
                cursor = connection.connection.cursor()
                
                print("Executando carga de veículos elétricos...")
                cursor.executescript(sql_eletricos)
                
                # Executa o script de combustão
                print("Executando carga de veículos a combustão...")
                cursor.executescript(sql_combustao)
            
            print("Registros importados com sucesso!")
            
    except Exception as e:
        print(f"\nFalha ao carregar dados iniciais do SQL: {e}")
    finally:
        session.close()

# Executa automaticamente a verificação e carga toda vez que o projeto inicia ou reinicia (reload)
carregar_dados_iniciais()
