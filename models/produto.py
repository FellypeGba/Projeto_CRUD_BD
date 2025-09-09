from db.connection import get_connection

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
  cur = conn.cursor()
  cur.execute("SELECT * FROM produto;")
  rows = cur.fetchall()
  cur.close()
  conn.close()
  return rows

def atualizar(id, nome, descricao, qtd, valor, ano, codEquipe, codPiloto):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    UPDATE produto
    SET nome=%s, descricao=%s, qtd=%s, valor=%s, ano_temporada=%s, codEquipe=%s,codPiloto=%s
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
  """, (id))
  conn.commit()
  cur.close()
  conn.close()
