from flask import redirect
from flask_openapi3.openapi import OpenAPI
from flask_openapi3.models.info import Info
from flask_openapi3.models.tag import Tag
from flask_cors import CORS
from rotas import bp_usuario, bp_veiculo, bp_veiculo_ev, bp_comparativo

info = Info(title="Petrowatts - comparador veículos à combustão x elétricos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
usuario_tag = Tag(name="Usuário", description="Adição, visualização e remoção de usuários à base")
veiculo_eletrico_tag = Tag(name="Veículos Elétricos", description="Consultas de veículos elétricos")
veiculo_combustao_tag = Tag(name="Veículos a Combustão", description="Consultas de marcas, modelos e anos da base")
comparativo_tag = Tag(name="Comparativo", description="Rotas de comparativo de custos energéticos")

# Registra os Blueprints na aplicação OpenAPI principal
app.register_api(bp_usuario)
app.register_api(bp_veiculo)
app.register_api(bp_veiculo_ev)
app.register_api(bp_comparativo)

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para documentação Swagger."""
    return redirect('/openapi/swagger')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)