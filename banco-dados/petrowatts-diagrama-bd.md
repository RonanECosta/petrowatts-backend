# petrowwats-diagrama-bd documentation

## Summary

- [petrowwats-diagrama-bd documentation](#petrowwats-diagrama-bd-documentation)
  - [Summary](#summary)
  - [Introdução](#introdução)
  - [Estrutura de tabelas](#estrutura-de-tabelas)
    - [usuarios](#usuarios)
    - [usuarios\_carros](#usuarios_carros)
    - [fabricantes](#fabricantes)
    - [carros\_eletricos](#carros_eletricos)
    - [carros\_combustao](#carros_combustao)
    - [acessorios](#acessorios)
    - [acessorio\_carro\_eletrico](#acessorio_carro_eletrico)
  - [Relacionamentos](#relacionamentos)
  - [Diagrama do Banco de Dados](#diagrama-do-banco-de-dados)

## Introdução

Esse diagrama representa a estrutura do banco de dados do Produto Mínimo Viável (MVP) do sistema Petrowatt.

A modelagem foi desenvolvida para armazenar dados necessários para o funcionamento do sistema com cálculos de investimentos e projeções de retorno financeiro na transição do uso pessoal de veículos a combustão para modelos elétricos.

## Estrutura de tabelas

### usuarios

| Nome | Tipo | Configurações | References |
| --- | --- | --- | --- |
| **id** | INT | PK, not null, autoincrement | |
| **nome** | VARCHAR(255) | not null | |
| **estado** | VARCHAR(2) | not null | |
| **cpf** | VARCHAR(11) | unique, not null | |

### usuarios_carros

| Nome | Tipo | Configurações | References |
| --- | --- | --- | --- |
| **id** | INT | PK, not null, autoincrement | |
| **id_usuario** | INTEGER | not null | fk_usuarios_carros_id_usuario_usuarios |
| **id_carro_combustao** | INTEGER | not null | fk_usuarios_carros_id_carro_combustao_carros_combustao |
| **km_mensal** | INTEGER | not null | |

### fabricantes

| Nome | Tipo | Configurações | References |
| --- | --- | --- | --- |
| **id** | INT | PK, not null, autoincrement | |
| **fabricante** | VARCHAR(255) | not null | |

### carros_eletricos

| Nome | Tipo | Configurações | References |
| --- | --- | --- | --- |
| **id** | INT | PK, not null, autoincrement | |
| **id_fabricante** | INTEGER | not null | fk_carros_eletricos_id_fabricante_fabricantes |
| **modelo** | VARCHAR(255) | not null | |
| **valor_compra** | NUMERIC(9, 2) | not null | |
| **consumo_mj_km** | NUMERIC(3, 2) | not null | |
| **potencia_cv** | INTEGER | not null | |
| **autonomia_km** | INTEGER | not null | |
| **capacidade_bat_kwh** | NUMERIC(6, 2) | not null | |
| **porta_malas_litros** | INTEGER | not null | |
| **necessario_infra** | BOOLEAN | not null | |
| **thumbnail** | MEDIUMBLOB | null | |

### carros_combustao

| Nome | Tipo | Configurações | References |
| --- | --- | --- | --- |
| **id** | INT | PK, not null, autoincrement | |
| **id_fabricante** | INTEGER | not null | fk_carros_combustao_id_fabricante_fabricantes |
| **modelo** | VARCHAR(255) | not null | |
| **valor_revenda** | NUMERIC(9, 2) | not null | |
| **consumo** | NUMERIC(3, 1) | not null | |
| **ano** | NUMERIC(4) | not null | |

### acessorios

| Nome | Tipo | Configurações | References |
| --- | --- | --- | --- |
| **id** | INT | PK, not null, autoincrement | |
| **nome** | VARCHAR(255) | not null | |

### acessorio_carro_eletrico

| Nome | Tipo | Configurações | References |
| --- | --- | --- | --- |
| **id** | INT | PK, not null, autoincrement | |
| **id_carro_eletrico** | INTEGER | not null | fk_acessorio_carro_eletrico_id_carro_eletrico_carros_eletricos |
| **id_acessorio** | INTEGER | not null | fk_acessorio_carro_eletrico_id_acessorio_acessorios |
| **valor_tamanho** | REAL | not null | |

## Relacionamentos

- **carros_combustao to fabricantes**: many_to_one (id_fabricante -> fabricantes.id)
- **carros_eletricos to fabricantes**: many_to_one (id_fabricante -> fabricantes.id)
- **usuarios_carros to usuarios**: many_to_one (id_usuario -> usuarios.id)
- **usuarios_carros to carros_combustao**: many_to_one (id_carro_combustao -> carros_combustao.id)
- **acessorio_carro_eletrico to acessorios**: many_to_one (id_acessorio -> acessorios.id)
- **acessorio_carro_eletrico to carros_eletricos**: many_to_one (id_carro_eletrico -> carros_eletricos.id)

## Diagrama do Banco de Dados

```mermaid
erDiagram
    fabricantes ||--o{ carros_combustao : "possui"
    fabricantes ||--o{ carros_eletricos : "possui"
    usuarios ||--o{ usuarios_carros : "possui"
    carros_combustao ||--o{ usuarios_carros : "pertence a"
    carros_eletricos ||--o{ acessorio_carro_eletrico : "possui"
    acessorios ||--o{ acessorio_carro_eletrico : "associado a"

    usuarios {
        INT id PK
        VARCHAR nome
        VARCHAR estado
        VARCHAR cpf
    }

    usuarios_carros {
        INT id PK
        INT id_usuario FK
        INT id_carro_combustao FK
        INT km_mensal
    }

    fabricantes {
        INT id PK
        VARCHAR fabricante
    }

    carros_eletricos {
        INT id PK
        INT id_fabricante FK
        VARCHAR modelo
        NUMERIC valor_compra
        NUMERIC consumo_mj_km
        INT potencia_cv
        INT autonomia_km
        NUMERIC capacidade_bat_kwh
        INT porta_malas_litros
        BOOLEAN necessario_infra
        MEDIUMBLOB thumbnail
    }

    carros_combustao {
        INT id PK
        INT id_fabricante FK
        VARCHAR modelo
        NUMERIC valor_revenda
        NUMERIC consumo
        NUMERIC ano
    }

    acessorios {
        INT id PK
        VARCHAR nome
    }

    acessorio_carro_eletrico {
        INT id PK
        INT id_carro_eletrico FK
        INT id_acessorio FK
        REAL valor_tamanho
    }
