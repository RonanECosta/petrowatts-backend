CREATE TABLE IF NOT EXISTS fabricantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fabricante VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS carros_combustao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_fabricante INTEGER NOT NULL,
    modelo VARCHAR(255) NOT NULL,
    valor_revenda NUMERIC(9, 2) NOT NULL,
    consumo NUMERIC(3, 1) NOT NULL,
    ano NUMERIC(4) NOT NULL,
    FOREIGN KEY (id_fabricante) REFERENCES fabricantes (id) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS usuarios_carros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    id_carro_combustao INTEGER NOT NULL,
    km_mensal INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id),
    FOREIGN KEY (id_carro_combustao) REFERENCES carros_combustao (id) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS carros_eletricos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_fabricante INTEGER NOT NULL,
    modelo VARCHAR(255) NOT NULL,
    valor_compra NUMERIC(9, 2) NOT NULL,
    consumo_mj_km NUMERIC(3, 2) NOT NULL,
    potencia_cv INTEGER NOT NULL,
    autonomia_km INTEGER NOT NULL,
    capacidade_bat_kwh NUMERIC(6, 2) NOT NULL,
    porta_malas_litros INTEGER NOT NULL,
    necessario_infra BOOLEAN NOT NULL,
    thumbnail MEDIUMBLOB,
    FOREIGN KEY (id_fabricante) REFERENCES fabricantes (id) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS acessorios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS acessorio_carro_eletrico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_carro_eletrico INTEGER NOT NULL,
    id_acessorio INTEGER NOT NULL,
    valor_tamanho REAL NOT NULL,
    FOREIGN KEY (id_acessorio) REFERENCES acessorios (id) ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY (id_carro_eletrico) REFERENCES carros_eletricos (id) ON UPDATE NO ACTION ON DELETE NO ACTION
);