from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from src.database import db
from src.container import Container

# Import controllers
from src.controllers.produto_controller import ProdutoController
from src.controllers.usuario_controller import UsuarioController
from src.controllers.pedido_controller import PedidoController, RelatorioController

def create_app():
    container = Container()
    container.wire(modules=[
        "src.controllers.produto_controller",
        "src.controllers.usuario_controller",
        "src.controllers.pedido_controller"
    ])

    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    # Routes Produtos
    app.add_url_rule("/produtos", endpoint="listar_produtos", view_func=ProdutoController.listar, methods=["GET"])
    app.add_url_rule("/produtos/busca", endpoint="buscar_produtos", view_func=ProdutoController.listar, methods=["GET"])
    app.add_url_rule("/produtos/<int:id>", endpoint="buscar_produto_por_id", view_func=ProdutoController.buscar_por_id, methods=["GET"])
    app.add_url_rule("/produtos", endpoint="criar_produto", view_func=ProdutoController.criar, methods=["POST"])
    app.add_url_rule("/produtos/<int:id>", endpoint="atualizar_produto", view_func=ProdutoController.atualizar, methods=["PUT"])
    app.add_url_rule("/produtos/<int:id>", endpoint="deletar_produto", view_func=ProdutoController.deletar, methods=["DELETE"])

    # Routes Usuarios
    app.add_url_rule("/usuarios", endpoint="listar_usuarios", view_func=UsuarioController.listar, methods=["GET"])
    app.add_url_rule("/usuarios/<int:id>", endpoint="buscar_usuario_por_id", view_func=UsuarioController.buscar_por_id, methods=["GET"])
    app.add_url_rule("/usuarios", endpoint="criar_usuario", view_func=UsuarioController.criar, methods=["POST"])
    app.add_url_rule("/login", endpoint="login_usuario", view_func=UsuarioController.login, methods=["POST"])

    # Routes Pedidos
    app.add_url_rule("/pedidos", endpoint="criar_pedido", view_func=PedidoController.criar, methods=["POST"])
    app.add_url_rule("/pedidos", endpoint="listar_todos_pedidos", view_func=PedidoController.listar_todos, methods=["GET"])
    app.add_url_rule("/pedidos/usuario/<int:usuario_id>", endpoint="listar_pedidos_por_usuario", view_func=PedidoController.listar_por_usuario, methods=["GET"])
    app.add_url_rule("/pedidos/<int:pedido_id>/status", endpoint="atualizar_status_pedido", view_func=PedidoController.atualizar_status, methods=["PUT"])

    # Routes Relatorios
    app.add_url_rule("/relatorios/vendas", endpoint="relatorio_vendas", view_func=RelatorioController.vendas, methods=["GET"])

    @app.route("/health")
    def health_check():
        return jsonify({"status": "ok"}), 200

    @app.route("/")
    def index():
        return jsonify({"mensagem": "Bem-vindo à API da Loja Refatorada (MVC)"}), 200

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=app.config["DEBUG"])
