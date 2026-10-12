CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    apartamento VARCHAR(50) NOT NULL
);

CREATE TABLE carregadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modelo VARCHAR(100) DEFAULT 'GoodWe HCA G2',
    localizacao VARCHAR(100) DEFAULT 'Estacionamento L1'
);

CREATE TABLE sessoes_recarga (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    carregador_id INT NOT NULL,
    data_hora_inicio DATETIME NOT NULL,
    data_hora_fim DATETIME NOT NULL,
    kwh_consumido DECIMAL(10, 2) NOT NULL,
    valor_kwh DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (carregador_id) REFERENCES carregadores(id)
);

CREATE TABLE cobrancas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    mes_referencia VARCHAR(7) NOT NULL,
    kwh_total DECIMAL(10, 2) NOT NULL,
    valor_energia DECIMAL(10, 2) NOT NULL,
    taxa_manutencao DECIMAL(10, 2) NOT NULL,
    valor_total_pagar DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
