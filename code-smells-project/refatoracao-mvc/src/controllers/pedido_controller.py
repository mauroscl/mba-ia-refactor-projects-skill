from flask import request, jsonify
from src.container import Container
from dependency_injector.wiring import Provide, inject

class PedidoController:
    @inject
    def criar(pedido_service = Provide[Container.pedido_service]):
        try:
            dados = request.get_json()
            pedido = pedido_service.criar(dados)
            return jsonify({"dados": pedido.to_dict(), "mensagem": "Pedido criado com sucesso", "sucesso": True}), 201
        except ValueError as ve:
            return jsonify({"erro": str(ve), "sucesso": False}), 400
        except Exception as e:
            return jsonify({"erro": str(e), "sucesso": False}), 500

    @inject
    def listar_todos(pedido_service = Provide[Container.pedido_service]):
        try:
            pedidos = pedido_service.listar_todos()
            return jsonify({"dados": [p.to_dict() for p in pedidos], "sucesso": True}), 200
        except Exception as e:
            return jsonify({"erro": str(e), "sucesso": False}), 500

    @inject
    def listar_por_usuario(usuario_id, pedido_service = Provide[Container.pedido_service]):
        try:
            pedidos = pedido_service.listar_por_usuario(usuario_id)
            return jsonify({"dados": [p.to_dict() for p in pedidos], "sucesso": True}), 200
        except Exception as e:
            return jsonify({"erro": str(e), "sucesso": False}), 500

    @inject
    def atualizar_status(pedido_id, pedido_service = Provide[Container.pedido_service]):
        try:
            dados = request.get_json()
            status = dados.get("status")
            pedido_service.atualizar_status(pedido_id, status)
            return jsonify({"mensagem": "Status atualizado", "sucesso": True}), 200
        except ValueError as ve:
            return jsonify({"erro": str(ve), "sucesso": False}), 400
        except Exception as e:
            return jsonify({"erro": str(e), "sucesso": False}), 500

class RelatorioController:
    @inject
    def vendas(relatorio_service = Provide[Container.relatorio_service]):
        try:
            relatorio = relatorio_service.gerar_relatorio_vendas()
            return jsonify({"dados": relatorio, "sucesso": True}), 200
        except Exception as e:
            return jsonify({"erro": str(e), "sucesso": False}), 500
