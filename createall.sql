-- Banco
CREATE DATABASE IF NOT EXISTS storeF1;

-- Tabelas

CREATE TABLE IF NOT EXISTS cliente (
  codCliente seriaL NOT NULL,
  nomeCliente character varying(80) NOT NULL,
  emailCliente character varying(80) UNIQUE NOT NULL,
  cpfCliente character(11) UNIQUE NOT NULL,
  dataNasc date NOT NULL,
  telefoneCliente character(11),
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

CREATE TABLE IF NOT EXISTS produto(
  codProd serial NOT NULL,
  nomeProd character varying(50) NOT NULL,
  descricao text,
  qtd integer NOT NULL,
  valor numeric(10, 2) NOT NULL,
  ano_temporada integer,
  codEquipe integer,
  codPiloto integer,
  PRIMARY KEY (codProd),
	FOREIGN KEY (codEquipe) REFERENCES equipe(codEquipe),
  FOREIGN KEY (codPiloto) REFERENCES piloto(codPiloto)
);

CREATE TABLE IF NOT EXISTS venda (
  codVenda serial NOT NULL,
  dataVenda timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  valorVenda numeric(10, 2) NOT NULL,
  statusVenda character varying(30) DEFAULT 'Processando',
  codCliente integer NOT NULL,
  PRIMARY KEY (codVenda),
	FOREIGN KEY (codCliente) REFERENCES cliente(codCliente)
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

