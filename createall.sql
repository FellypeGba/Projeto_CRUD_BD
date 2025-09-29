-- Banco
CREATE DATABASE IF NOT EXISTS storeF1;

-- Cria o tipo ENUM para o status do pagamento
CREATE TYPE statusPagamento_tipo AS ENUM ('Confirmado', 'Pendente', 'Recusado', 'Cancelado');

-- Tabelas
CREATE TABLE IF NOT EXISTS cliente (
  codCliente serial NOT NULL,
  nomeCliente character varying(80) NOT NULL,
  emailCliente character varying(80) UNIQUE NOT NULL,
  cpfCliente character(11) UNIQUE NOT NULL,
  dataNasc date NOT NULL,
  telefoneCliente character(11),
  timeAmado character varying(50) NOT NULL,
  onePiece boolean NOT NULL,
  cidade character varying(50) NOT NULL,
  PRIMARY KEY (codCliente)
);

CREATE TABLE IF NOT EXISTS equipe (
  codEquipe serial NOT NULL,
  nomeEquipe character varying(100) UNIQUE NOT NULL,
  PRIMARY KEY (codEquipe)
);

CREATE TABLE IF NOT EXISTS piloto (
  codPiloto serial NOT NULL,
  nomePiloto character varying(80) NOT NULL,
  numero integer,
  codEquipe integer NOT NULL,
  PRIMARY KEY (codPiloto),
  FOREIGN KEY (codEquipe) REFERENCES equipe(codEquipe)
);

CREATE TABLE IF NOT EXISTS fabricante (
  codFabricante serial NOT NULL,
  nomeFabricante character varying(100) UNIQUE NOT NULL,
  cidadeFabricante character varying(50) NOT NULL,
  PRIMARY KEY (codFabricante)
);

CREATE TABLE IF NOT EXISTS produto(
  codProd serial NOT NULL,
  nomeProd character varying(50) NOT NULL,
  descricao text,
  qtd integer NOT NULL,
  valor numeric(10, 2) NOT NULL,
  ano_temporada integer,
  categoria character varying(50) NOT NULL,
  codEquipe integer,
  codPiloto integer,
  codFabricante integer NOT NULL,
  PRIMARY KEY (codProd),
  FOREIGN KEY (codEquipe) REFERENCES equipe(codEquipe),
  FOREIGN KEY (codPiloto) REFERENCES piloto(codPiloto),
  FOREIGN KEY (codFabricante) REFERENCES fabricante(codFabricante)
);

CREATE TABLE IF NOT EXISTS vendedor (
  codVendedor SERIAL PRIMARY KEY,
  nomeVendedor VARCHAR(100) NOT NULL,
  emailVendedor VARCHAR(100) UNIQUE NOT NULL,
  dataNasc date NOT NULL,
  telefoneVendedor character(11)
);

CREATE TABLE IF NOT EXISTS pagamento (
  codPagamaneto SERIAL PRIMARY KEY,
  nomePagamento VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS venda (
  codVenda serial NOT NULL,
  dataVenda timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  valorVenda numeric(10, 2) NOT NULL,
  codPagamaneto INTEGER NOT NULL,
  codCliente integer NOT NULL,
  codVendedor INTEGER NOT NULL,
  statusPagamento statusPagamento_tipo,
  PRIMARY KEY (codVenda),
  FOREIGN KEY (codCliente) REFERENCES cliente(codCliente),
  FOREIGN KEY (codVendedor) REFERENCES vendedor(codVendedor),
  FOREIGN KEY (codPagamaneto) REFERENCES pagamento(codPagamaneto)
);

CREATE TABLE IF NOT EXISTS produtoVenda (
  codVenda integer NOT NULL,
  codProd integer NOT NULL,
  qtdVenda integer NOT NULL,
  valorUnitario numeric(10, 2) NOT NULL,
  PRIMARY KEY (codVenda, codProd),
  FOREIGN KEY (codVenda) REFERENCES venda(codVenda),
  FOREIGN KEY (codProd) REFERENCES produto(codProd)
);

-- STORE PROCEDURE E TRIGGER

CREATE OR REPLACE FUNCTION atualizar_estoque()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE produto
    SET qtd = qtd - NEW.qtdVenda
    WHERE codProd = NEW.codProd;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER atualizar_estoque_apos_venda
AFTER INSERT ON produtoVenda
FOR EACH ROW
EXECUTE FUNCTION atualizar_estoque();