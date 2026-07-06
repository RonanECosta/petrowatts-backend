CREATE TABLE IF NOT EXISTS "usuarios" (
    "id" INTEGER NOT NULL,
    "nome" VARCHAR NOT NULL,
    "estado" VARCHAR NOT NULL,
    "cpf" VARCHAR UNIQUE NOT NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("id") REFERENCES "usuarios_carros" ("id_usuario") ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "usuarios_carros" (
    "id" INTEGER NOT NULL,
    "id_usuario" INTEGER NOT NULL,
    "id_carro" INTEGER NOT NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("id_usuario") REFERENCES "usuarios" ("id"),
    FOREIGN KEY ("id_carro") REFERENCES "carros_combustao" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "fabricantes" (
    "id" INTEGER NOT NULL,
    "fabricante" VARCHAR NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "carros_eletricos" (
    "id" INTEGER NOT NULL,
    "id_fabricante" INTEGER NOT NULL,
    "valor_compra" NUMERIC(9, 2) NOT NULL,
    "consumo_mj_km" NUMERIC(3, 2) NOT NULL,
    "potencia_cv" INTEGER NOT NULL,
    "autonomia_km" INTEGER NOT NULL,
    "capacidade_bat_kwh" NUMERIC(6, 2) NOT NULL,
    "porta_malas_litros" INTEGER NOT NULL,
    "necessario_infra" BOOLEAN NOT NULL,
    "thumbnail" BLOB,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("id_fabricante") REFERENCES "fabricantes" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "carros_combustao" (
    "id" INTEGER NOT NULL,
    "id_fabricante" INTEGER NOT NULL,
    "valor_revenda" NUMERIC(9, 2) NOT NULL,
    "consumo" NUMERIC(3, 1) NOT NULL,
    "ano" NUMERIC NOT NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("id_fabricante") REFERENCES "fabricantes" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "acessorios" (
    "id" INTEGER NOT NULL,
    "nome" VARCHAR NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "acessorio_carro_eletrico" (
    "id" INTEGER NOT NULL,
    "id_carro" INTEGER NOT NULL,
    "id_acessorio" INTEGER NOT NULL,
    "valor_tamanho" REAL NOT NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("id_acessorio") REFERENCES "acessorios" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY ("id_carro") REFERENCES "carros_eletricos" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);