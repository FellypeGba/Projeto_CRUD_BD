from db.connection import get_connection
import psycopg2.extras

def inserir(nome, descricao, qtd, valor, ano, categoria, codEquipe, codPiloto, codFabricante):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    INSERT INTO produto (nomeProd, descricao, qtd, valor, ano_temporada, categoria, codEquipe, codPiloto, codFabricante)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
  """, (nome, descricao, qtd, valor, ano, categoria, codEquipe, codPiloto, codFabricante))
  conn.commit()
  cur.close()
  conn.close()

def listar():
  conn = get_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("""
    SELECT 
      p.codProd, p.nomeProd, p.descricao, p.qtd, p.valor, p.ano_temporada, 
      p.categoria, p.codEquipe, p.codPiloto, 
      f.nomeFabricante AS fabricante
    FROM produto p
    INNER JOIN fabricante f ON p.codFabricante = f.codFabricante;
  """)
  produtos = [dict(row) for row in cur.fetchall()]
  cur.close()
  conn.close()
  return produtos

def atualizar(id, nome, descricao, qtd, valor, ano, categoria, codEquipe, codPiloto, codFabricante):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("""
    UPDATE produto
    SET nomeProd=%s, descricao=%s, qtd=%s, valor=%s, ano_temporada=%s, categoria=%s, codEquipe=%s, codPiloto=%s, codFabricante=%s
    WHERE codProd=%s;
  """, (nome, descricao, qtd, valor, ano, categoria, codEquipe, codPiloto, codFabricante, id))
  conn.commit()
  cur.close()
  conn.close()

def filtrarNome(nome):
  conn = get_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  buscaNome = f"%{nome}%"
  cur.execute("""
    SELECT 
      p.codProd, p.nomeProd, p.descricao, p.qtd, p.valor, p.ano_temporada, 
      p.categoria, p.codEquipe, p.codPiloto, 
      f.nomeFabricante AS fabricante
    FROM produto p
    INNER JOIN fabricante f ON p.codFabricante = f.codFabricante
    WHERE p.nomeProd ILIKE (%s);
  """, (buscaNome,))

  produtos = [dict(row) for row in cur.fetchall()]
  conn.commit()
  cur.close()
  conn.close()
  return produtos

def filtrar_produtos(nome=None, categoria=None, preco_min=None, preco_max=None, fabricadoMari=False, estoque_baixo=False):
  conn = get_connection()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

  query_base = """
    SELECT 
      p.codProd, p.nomeProd, p.descricao, p.qtd, p.valor, p.ano_temporada, 
      p.categoria, p.codEquipe, p.codPiloto, 
      f.nomeFabricante AS fabricante
    FROM produto p
    INNER JOIN fabricante f ON p.codFabricante = f.codFabricante
  """

  condicoes = []
  parametros = []

  if nome:
    condicoes.append("p.nomeProd ILIKE %s")
    parametros.append(f"%{nome}%")
  
  if categoria:
    condicoes.append("p.categoria ILIKE %s")
    parametros.append(f"%{categoria}%")

  if preco_min is not None:
    condicoes.append("p.valor >= %s")
    parametros.append(preco_min)
  
  if preco_max is not None:
    condicoes.append("p.valor <= %s")
    parametros.append(preco_max)
  
  if fabricadoMari:
    condicoes.append("f.cidadeFabricante = %s")
    parametros.append("Mari")

  if estoque_baixo:
    condicoes.append("p.qtd < %s")
    parametros.append(5)

  if condicoes:
    query_final = query_base + " WHERE " + " AND ".join(condicoes)
  else:
    query_final = query_base
  
  cur.execute(query_final, tuple(parametros))

  produtos = [dict(row) for row in cur.fetchall()]
  cur.close()
  conn.close()
  return produtos

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
