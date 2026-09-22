-- 1. CARGA DA TABELA: fabricantes
INSERT INTO
    fabricantes (id, fabricante)
VALUES (1, 'BYD'),
    (2, 'GWM'),
    (3, 'Renault'),
    (4, 'JAC'),
    (5, 'Caoa Chery');

-- 2. CARGA DA TABELA: acessorios
-- Cadastrando apenas os nomes genéricos dos acessórios na tabela base
INSERT INTO
    acessorios (id, nome)
VALUES (
        1,
        'Central Multimídia (Polegadas)'
    ),
    (
        2,
        'Pontos de Fixação ISOFIX (Quantidade)'
    ),
    (
        3,
        'Airbags de Cabine (Quantidade)'
    ),
    (
        4,
        'Teto Solar Panorâmico (Área em m2)'
    ),
    (
        5,
        'Câmeras de Estacionamento (Quantidade de Lentes)'
    );

-- 3. CARGA DA TABELA: carros_eletricos
-- Modelos 100% elétricos reais vendidos no Brasil por menos de R$ 200.000
INSERT INTO
    carros_eletricos (
        id,
        id_fabricante,
        modelo,
        valor_compra,
        consumo_mj_km,
        potencia_cv,
        autonomia_km,
        capacidade_bat_kwh,
        porta_malas_litros,
        necessario_infra,
        thumbnail
    )
VALUES (
        1,
        1,
        'Dolphin Mini 4L',
        119800.00,
        0.41,
        75,
        280.0,
        38.0,
        230,
        0,
        NULL
    ), -- BYD Dolphin Mini (4 lugares)
    (
        2,
        1,
        'Dolphin Mini 5L',
        121800.00,
        0.41,
        75,
        280.0,
        38.0,
        230,
        0,
        NULL
    ), -- BYD Dolphin Mini (5 lugares)
    (
        3,
        1,
        'Dolphin GS',
        149800.00,
        0.42,
        95,
        291.0,
        44.9,
        345,
        1,
        NULL
    ), -- BYD Dolphin GS
    (
        4,
        1,
        'Dolphin Plus',
        184800.00,
        0.44,
        204,
        310.0,
        60.5,
        345,
        1,
        NULL
    ), -- BYD Dolphin Plus
    (
        5,
        2,
        'Ora 03 Skin',
        150000.00,
        0.44,
        171,
        232.0,
        48.0,
        228,
        1,
        NULL
    ), -- GWM Ora 03 Skin
    (
        6,
        2,
        'Ora 03 GT',
        184000.00,
        0.48,
        171,
        319.0,
        63.0,
        228,
        1,
        NULL
    ), -- GWM Ora 03 GT
    (
        7,
        3,
        'Kwid E-Tech',
        99990.00,
        0.44,
        65,
        185.0,
        26.8,
        290,
        0,
        NULL
    ), -- Renault Kwid E-Tech
    (
        8,
        3,
        'Megane E-Tech',
        135990.00,
        0.52,
        115,
        298.0,
        52.0,
        332,
        1,
        NULL
    ), -- Renault Megane E-Tech
    (
        9,
        4,
        'E-JS1',
        145900.00,
        0.48,
        62,
        205.0,
        30.2,
        250,
        0,
        NULL
    ), -- JAC E-JS1
    (
        10,
        5,
        'iCar',
        132990.00,
        0.43,
        61,
        161.0,
        25.0,
        166,
        0,
        NULL
    );
-- Caoa Chery iCar

-- 4. CARGA DA TABELA: acessorio_carro_eletrico
-- Agora a métrica/tamanho é informada diretamente na tabela pivot para cada variação real de veículo
INSERT INTO
    acessorio_carro_eletrico (
        id,
        id_carro_eletrico,
        id_acessorio,
        valor_tamanho
    )
VALUES
    -- Acessórios: BYD Dolphin Mini 4L (id_carro_eletrico: 1)
    (1, 1, 1, 10.2), -- Multimídia de 10.2
    (2, 1, 2, 2.0), -- 2 pontos Isofix
    (3, 1, 3, 4.0), -- 4 Airbags (específico desta versão)
    (4, 1, 5, 1.0), -- 1 Câmera de ré traseira

-- Acessórios: BYD Dolphin Mini 5L (id_carro_eletrico: 2)
(5, 2, 1, 10.2),
(6, 2, 2, 2.0),
(7, 2, 3, 6.0), -- 6 Airbags (ganho desta versão de 5 lugares)
(8, 2, 5, 1.0),

-- Acessórios: BYD Dolphin GS (id_carro_eletrico: 3)
(9, 3, 1, 12.8), -- Multimídia maior rotativa de 12.8
(10, 3, 2, 2.0),
(11, 3, 3, 6.0),
(12, 3, 5, 4.0), -- Sistema de câmeras 360° (4 lentes externas)

-- Acessórios: BYD Dolphin Plus (id_carro_eletrico: 4)
(13, 4, 1, 12.8),
(14, 4, 2, 2.0),
(15, 4, 3, 6.0),
(16, 4, 4, 1.1), -- Possui Teto Solar Panorâmico de 1.1m²
(17, 4, 5, 4.0),

-- Acessórios: GWM Ora 03 Skin (id_carro_eletrico: 5)
(18, 5, 1, 10.25), -- Tela de 10.25 integrada
(19, 5, 2, 2.0),
(20, 5, 3, 7.0), -- 7 Airbags (inclui o de joelho)
(21, 5, 5, 1.0),

-- Acessórios: GWM Ora 03 GT (id_carro_eletrico: 6)
(22, 6, 1, 10.25),
(23, 6, 2, 2.0),
(24, 6, 3, 7.0),
(25, 6, 4, 1.2), -- Teto solar panorâmico amplo nesta versão esportiva
(26, 6, 5, 4.0), -- Câmeras 360° completas

-- Acessórios: Renault Kwid E-Tech (id_carro_eletrico: 7)
(27, 7, 1, 7.0), -- Multimídia compacta de 7.0
(28, 7, 2, 2.0),
(29, 7, 3, 6.0),

-- Acessórios: Renault Megane E-Tech (id_carro_eletrico: 8)
(30, 8, 1, 12.0), -- Painel digital avançado com multimídia de 12.0
(31, 8, 2, 2.0),
(32, 8, 3, 7.0),
(33, 8, 5, 4.0),

-- Acessórios: JAC E-JS1 (id_carro_eletrico: 9)
(34, 9, 1, 10.25),
(35, 9, 2, 2.0),
(36, 9, 3, 2.0), -- Apenas 2 airbags frontais obrigatórios

-- Acessórios: Caoa Chery iCar (id_carro_eletrico: 10)
(37, 10, 1, 10.25), (38, 10, 2, 2.0), (39, 10, 3, 2.0);