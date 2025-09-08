-- Banco
CREATE DATABASE crud_flask;


-- Tabelas (
CREATE TABLE cliente (
  codcliente      SERIAL PRIMARY KEY,
  nomecliente    VARCHAR(80) NOT NULL,
  emailcliente    VARCHAR(80),
  cpf             CHAR(11) UNIQUE NOT NULL,
  datanasc        DATE,
  telefonecliente CHAR(11)
);

CREATE TABLE venda (
  codvenda    SERIAL PRIMARY KEY,
  datavenda   TIMESTAMPTZ NOT NULL,
  valorvenda  NUMERIC(10,2) NOT NULL,
  status      VARCHAR(30) NOT NULL,
  codcliente  INTEGER NOT NULL REFERENCES cliente(codcliente)
);

-- Ainda não existe tabela de produto; por isso codprod fica sem FK por enquanto
CREATE TABLE produtovenda (
  codvenda      INTEGER NOT NULL REFERENCES venda(codvenda) ON DELETE CASCADE,
  codprod       INTEGER NOT NULL,
  qtdvenda      INTEGER NOT NULL,
  valorunitario NUMERIC(10,2) NOT NULL,
  PRIMARY KEY (codvenda, codprod)
);
