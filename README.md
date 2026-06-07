# PetroWatts

Este é um MVP que será apresentado como Trabalho de Conclusão de Curso (TCC) da Pós-graduação da PUC-Rio.

## Funcionamento

O aplicativo contará com um cadastro para o usuário e, em seguida, o cadastro do seu carro a combustão com os seguintes dados:

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
