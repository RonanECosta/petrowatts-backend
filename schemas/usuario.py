from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated, Any, Optional, List
from model.usuario import Usuario

# Função auxiliar para garantir que qualquer número enviado vire string antes da validação
def coerce_to_string(v: Any) -> str:
    return str(v) if v is not None else "0"

# Criamos um tipo customizado que converte números para string automaticamente
CoercedStr = Annotated[str, BeforeValidator(coerce_to_string)]

class UsuarioSchema(BaseModel):
    """ Define como um novo usuário a ser inserido deve ser representado
    """
    cpf: CoercedStr = Field("12345678900", description="CPF do usuário (apenas números)")
    nome: str = "João"
    estado: str = "RJ"

class UsuarioViewSchema(BaseModel):
    """ Define como um usuário será retornado.
    """
    id: int = 1
    cpf: str = "12345678900"
    nome: str = "João"
    estado: str = "RJ"

def apresenta_usuarios(usuarios: List[Usuario]):
    """ Retorna uma representação do usuário seguindo o schema definido em
        UsuarioViewSchema.
    """
    result = []
    for usuario in usuarios:
        result.append({
            "id": usuario.id,
            "cpf": usuario.cpf,
            "nome": usuario.nome,
            "estado": usuario.estado,
        })

    return {"usuarios": result}

class UsuarioCarroQuerySchema(BaseModel):
    """ Define o parâmetro de busca obrigatório para localizar o usuário pelo CPF.
    """
    cpf: str = "12345678900"


class VeiculoVinculadoSchema(BaseModel):
    """ Define a estrutura de detalhes do carro que será retornada dentro do usuário.
    """
    id_fabricante: int = 1
    fabricante: str = "Chevrolet"
    modelo: str = "Onix"
    ano: int = 2020


class UsuarioCarroDetalhesViewSchema(BaseModel):
    """ Define a estrutura de retorno do usuário com seu veículo vinculado.
    """
    id_usuario: int = 1
    cpf: str = "12345678900"
    nome: str = "João"
    estado: str = "RJ"
    veiculo: VeiculoVinculadoSchema

class CadastroUsuarioCarroFormSchema(BaseModel):
    """ Define os campos necessários para cadastrar um usuário e vinculá-lo a um veículo.
        Os dados são enviados no formato de formulário tradicional (form).
    """
    nome: str = "João Silva"
    uf: str = "RJ"
    cpf: CoercedStr = Field("12345678900", description="CPF do usuário (apenas números)")
    id_fabricante: int = 7
    modelo: str = "Argo 1.0"
    ano: int = 2020
    km_mensal: int = 1234


class CadastroUsuarioCarroSucessoSchema(BaseModel):
    """ Define a estrutura da resposta retornada após um cadastro bem-sucedido.
    """
    message: str = "Usuário e veículo vinculados com sucesso!"
    id_usuario: int = 1

class AtualizarUsuarioCarroFormSchema(BaseModel):
    """ Define os campos de formulário para a atualização parcial.
        Apenas o id_usuario é obrigatório para localizar o registro.
    """
    id_usuario: int = Field(..., description="ID interno do usuário (Obrigatório)")
    nome: Optional[str] = Field("João da Silva Barbosa", description="Novo nome do usuário")
    uf: Optional[str] = Field("DF", description="Novo estado (UF) do usuário")
    cpf: Optional[CoercedStr] = Field("12345678900", description="Novo CPF do usuário (apenas números)")
    id_fabricante: Optional[int] = Field(7, description="ID do novo fabricante (requer modelo e ano)")
    modelo: Optional[str] = Field("Argo 1.0", description="Modelo do novo veículo (requer fabricante e ano)")
    ano: Optional[int] = Field(2020, description="Ano do novo veículo (requer fabricante e modelo)")
    km_mensal: Optional[int] = Field(1999, description="Nova rodagem mensal estimada")


class AtualizarUsuarioCarroSucessoSchema(BaseModel):
    """ Define o formato de resposta de sucesso na documentação """
    message: str = "Dados atualizados com sucesso."


class UsuarioDeleteQuerySchema(BaseModel):
    """ Define o parâmetro obrigatório na URL para a remoção do usuário via CPF.
    """
    id_usuario: int = Field(..., description="ID interno do usuário (Obrigatório)")

class UsuarioDeleteSucessoSchema(BaseModel):
    """ Define o formato de resposta após uma exclusão bem-sucedida.
    """
    message: str = "Usuário excluído com sucesso."
