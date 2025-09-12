from db.connection import get_connection
import psycopg2.extras

def inserir(nome, descricao, qtd, valor, ano, codEquipe, codPiloto):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    INSERT INTO produto (nomeProd, descricao, qtd, valor, ano_temporada, codEquipe, codPiloto)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
  """, (nome, descricao, qtd, valor, ano, codEquipe, codPiloto))
  conn.commit()
  cur.close()
  conn.close()

def listar():
  conn = get_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("SELECT * FROM produto;")
  produtos = [dict(row) for row in cur.fetchall()]
  cur.close()
  conn.close()
  return produtos

def atualizar(id, nome, descricao, qtd, valor, ano, codEquipe, codPiloto):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    UPDATE produto
    SET nomeProd=%s, descricao=%s, qtd=%s, valor=%s, ano_temporada=%s, codEquipe=%s,codPiloto=%s
    WHERE codProd=%s;
  """, (nome, descricao, qtd, valor, ano, codEquipe, codPiloto, id))
  conn.commit()
  cur.close()
  conn.close()

def deletar(id):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    DELETE FROM produto
    WHERE codProd=%s
  """, (id,))
  conn.commit()
  cur.close()
  conn.close()
