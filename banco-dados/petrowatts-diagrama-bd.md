
# petrowwats-diagrama-bd documentation

## Summary

- [Introdução](#introdução)
- [Estrutura de tabelas](#estrutura-de-tabelas)
  - [usuarios](#usuarios)
  - [usuarios_carros](#usuarios_carros)
  - [fabricantes](#fabricantes)
  - [carros_eletricos](#carros_eletricos)
  - [carros_combustao](#carros_combustao)
  - [acessorios](#acessorios)
  - [acessorio_carro_eletrico](#acessorio_carro_eletrico)
- [Relacionomentos](#relacionomentos)
- [Diagrama do Banco de Dados](#diagrama-do-banco-de-dados)

## Introdução

Esse diagrama representa a estrutura do banco de dados do Produto Mínimo Viável (MVP) do sistema Petrowatt.

A modelagem foi desenvolvida para armazenar dados necessários para o funcionomento do sistema com cálculos de investimentos e projeções de retorno financeiro na transição do uso pessoal de veículos a combustão para modelos elétricos.

## Estrutura de tabelas

### usuarios

| Nome       | Tipo         | Configurações                  | References                     |
| ---------- | ------------ | ------------------------------ | ------------------------------ |
| **id**     | INTEGER      | 🔑 PK, not null, autoincrement | fk_usuarios_id_usuarios_carros |
| **cpf**    | VARCHAR(11)  | unique                         |                                |
| **nome**   | VARCHAR(255) | not null                       |                                |
| **estado** | VARCHAR(2)   | not null                       |                                |  

### usuarios_carros

| Nome           | Tipo    | Configurações                  | References                                   |
| -------------- | ------- | ------------------------------ | -------------------------------------------- |
| **id**         | INTEGER | 🔑 PK, not null, autoincrement |                                              |
| **id_usuario** | INTEGER | not null                       |                                              |
| **id_carro**   | INTEGER | not null                       | fk_usuarios_carros_id_carro_carros_combustao |  

### fabricantes

| Nome           | Tipo         | Configurações                  | References |
| -------------- | ------------ | ------------------------------ | ---------- |
| **id**         | INTEGER      | 🔑 PK, not null, autoincrement |            |
| **fabricante** | VARCHAR(255) | not null                       |            |

### carros_eletricos

| Nome                   | Tipo    | Configurações                  | References                                    |
| ---------------------- | ------- | ------------------------------ | --------------------------------------------- |
| **id**                 | INTEGER | 🔑 PK, not null, autoincrement |                                               |
| **id_fabricante**      | INTEGER | not null                       | fk_carros_eletricos_id_fabricante_fabricantes |
| **valor_compra**       | REAL    | not null                       |                                               |
| **consumo_mj_km**      | NUMERIC | not null                       |                                               |
| **potencia_cv**        | INTEGER | not null                       |                                               |
| **autonomia_km**       | REAL    | not null                       |                                               |
| **capacidade_bat_kwh** | REAL    | not null                       |                                               |
| **porta_malas_litros** | INTEGER | not null                       |                                               |
| **necessario_infra**   | BOOLEAN | not null                       |                                               |
| **thumbnail**          | BLOB    | null                           |                                               |

### carros_combustao

| Nome              | Tipo    | Configurações                  | References                                    |
| ----------------- | ------- | ------------------------------ | --------------------------------------------- |
| **id**            | INTEGER | 🔑 PK, not null, autoincrement |                                               |
| **id_fabricante** | INTEGER | not null                       | fk_carros_combustao_id_fabricante_fabricantes |
| **valor_revenda** | REAL    | not null                       |                                               |
| **consumo**       | NUMERIC | not null                       |                                               |
| **ano**           | NUMERIC | not null                       |                                               |

### acessorios

| Nome     | Tipo         | Configurações                  | References |
| -------- | ------------ | ------------------------------ | ---------- |
| **id**   | INTEGER      | 🔑 PK, not null, autoincrement |            |
| **nome** | VARCHAR(255) | not null                       |            |

### acessorio_carro_eletrico

| Nome              | Tipo    | Configurações                  | References                                            |
| ----------------- | ------- | ------------------------------ | ----------------------------------------------------- |
| **id**            | INTEGER | 🔑 PK, not null, autoincrement |                                                       |
| **id_carro**      | INTEGER | not null                       | fk_acessorio_carro_eletrico_id_carro_carros_eletricos |
| **id_acessorio**  | INTEGER | not null                       | fk_acessorio_carro_eletrico_id_acessorio_acessorios   |
| **valor_tamanho** | REAL    | not null                       |                                                       |

## Relacionomentos

- **carros_combustao to fabricantes**: many_to_one
- **carros_eletricos to fabricantes**: many_to_one
- **usuarios_carros to carros_combustao**: many_to_one
- **usuarios to usuarios_carros**: one_to_many
- **acessorio_carro_eletrico to acessorios**: many_to_one
- **acessorio_carro_eletrico to carros_eletricos**: many_to_one

## Diagrama do Banco de Dados

```mermaid
erDiagram
 carros_combustao }o--|| fabricantes : references
 carros_eletricos }o--|| fabricantes : references
 usuarios_carros }o--|| carros_combustao : references
 usuarios ||--o{ usuarios_carros : references
 acessorio_carro_eletrico }o--|| acessorios : references
 acessorio_carro_eletrico }o--|| carros_eletricos : references

 usuarios {
  INTEGER id
  VARCHAR(255) Nome
  VARCHAR(2) Estado
 }

 usuarios_carros {
  INTEGER id
  INTEGER id_usuario
  INTEGER id_carro
 }

 fabricantes {
  INTEGER id
  VARCHAR(255) fabricante
 }

 carros_eletricos {
  INTEGER id
  INTEGER id_fabricante
  REAL valor_compra
  NUMERIC consumo_mj_km
  INTEGER potencia_cv
  REAL autonomia_km
  REAL capacidade_bat_kwh
  INTEGER porta_malas_litros
  BOOLEAN necessario_infra
  BLOB thumbnail
 }

 carros_combustao {
  INTEGER id
  INTEGER id_fabricante
  REAL valor_revenda
  NUMERIC consumo
  NUMERIC ano
 }

 acessorios {
  INTEGER id
  VARCHAR(255) nome
 }

 acessorio_carro_eletrico {
  INTEGER id
  INTEGER id_carro
  INTEGER id_acessorio
  REAL valor_tamanho
 }
