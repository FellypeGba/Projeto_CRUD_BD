from flask import Flask
#from routes import routes
#from routes.routes import routes
from routes.cliente_routes import cliente_bp
from routes.equipe_routes import equipe_bp
from routes.piloto_routes import piloto_bp
from routes.produto_routes import produto_bp
from routes.produtoVenda_routes import produto_venda_bp

lista_registros = [cliente_bp, equipe_bp, piloto_bp, produto_bp, produto_venda_bp]

app = Flask(__name__)
for registro in lista_registros:
    app.register_blueprint(registro) #registrando cada uma das rotas

#app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)
