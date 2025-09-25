from db.connection import get_connection
import psycopg2.extras

#criar vendedor
def criar(nome, email, dataNasc, telefoneVendedor):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO vendedor (nomeVendedor, emailVendedor, dataNasc, telefoneVendedor)
        VALUES (%s, %s, %s, %s)
        RETURNING codVendedor;
    """, (nome, email, dataNasc, telefoneVendedor))
    codVendedor = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return codVendedor

#listando os vendedores
def listar():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM vendedor;")
    vendedores = [dict(row) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return vendedores