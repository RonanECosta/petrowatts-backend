# PetroWatts

Este é um MVP que será apresentado como Trabalho de Conclusão de Curso (TCC) da Pós-graduação da PUC-Rio.

## Funcionamento

O aplicativo contará com um cadastro para o usuário, seu estado de residência e, em seguida, o cadastro do seu carro a combustão com os seguintes dados:

* Marca
* Modelo
* Ano
* Consumo médio (km/l)
* Rodagem usual mensal

A partir dos dados preenchidos, o sistema irá calcular e exibir:

* Valor estimado de investimento para a troca por um veículo elétrico
* Economia gerada em combustível
* Impacto de gastos na conta de luz
* Redução de emissões de carbono
* Tempo estimado para recuperação do investimento inicial (payback)

Para o correto funcionamento das funcionalidades acima, serão necessário o manuseio dos seguintes dados:

* usuário
* carro possuído por usuário
* carro à combustão (marca, modelo, ano, consumo, imagem, valor revenda FIPE)
* carro elétricos (marca, modelo, valor compra, consumo)
* dados de preços do Kwh (Região, preço Kwh)

## Tecnologias Utilizadas

* **Frontend:** HTML, Bootstrap, CSS e Flask
* **Backend:** Python e banco de dados SQLite
* **Documentação:** Swagger para documentar as APIs

## Diagrama BD

* <https://www.drawdb.app/editor?shareId=78117b3e80c9cd07b123d5c4a1aba217>

## Preparação para Execução

Conforme explicado nas aulas, é de suma importância a utilização de ambientes virtuais para evitar conflitos de bibliotecas e outras dependências utilizadas no projeto versus a configuração global do seu computador.

Siga os passos abaixo para configurar o ambiente virtual e instalar as dependências do projeto.

### Criação do ambiente

Abra o terminal, navegue até a raiz do projeto e execute:
``bash
python -m venv .venv
``

Escolha o comando de acordo com o terminal que você está utilizando:

* **PowerShell:**

  ```powershell
  .venv\Scripts\Activate.ps1
  ```

* **Prompt de Comando/CMD:**

  ```cmd
  .venv\Scripts\activate.bat
  ```

> *Nota: O prefixo `(.venv)` deverá aparecer no início da linha, indicando assim que o ambiente está ativo.*

### Instalação das dependências

Com o ambiente virtual ativado, instale todos os pacotes necessários:

```bash
pip install -r requirements.txt
```

**Caso seja necessário** instalar uma nova biblioteca (por exemplo, o Pydantic), utilize:

```bash
pip install pydantic
```

Sempre que instalar um novo pacote, atualize o arquivo de dependências para o Git com o comando:

```bash
pip freeze > requirements.txt
```
