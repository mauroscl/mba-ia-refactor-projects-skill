from flask import request, jsonify
from src.container import Container
from dependency_injector.wiring import Provide, inject

class ProdutoController:
    @inject
    def listar(produto_service = Provide[Container.produto_service]):
        try:
            termo = request.args.get("q", "")
            categoria = request.args.get("categoria", None)
            preco_min = request.args.get("preco_min", None, type=float)
            preco_max = request.args.get("preco_max", None, type=float)

            if termo or categoria or preco_min is not None or preco_max is not None:
                produtos = produto_service.buscar(termo, categoria, preco_min, preco_max)
            else:
                produtos = produto_service.listar()

            return jsonify({"dados": [p.to_dict() for p in produtos], "total": len(produtos), "sucesso": True}), 200
        except Exception as e:
            return jsonify({"erro": str(e), "sucesso": False}), 500

    @inject
    def buscar_por_id(id, produto_service = Provide[Container.produto_service]):
        try:
            produto = produto_service.buscar_por_id(id)
            if produto:
                return jsonify({"dados": produto.to_dict(), "sucesso": True}), 200
            return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404
        except Exception as e:
            return jsonify({"erro": str(e), "sucesso": False}), 500

    @inject
    def criar(produto_service = Provide[Container.produto_service]):
        try:
            dados = request.get_json()
            if not dados:
                return jsonify({"erro": "Dados inválidos", "sucesso": False}), 400

            produto = produto_service.criar(dados)
            return jsonify({"dados": {"id": produto.id}, "mensagem": "Produto criado", "sucesso": True}), 201
        except ValueError as ve:
            return jsonify({"erro": str(ve), "sucesso": False}), 400
        except Exception as e:
            return jsonify({"erro": str(e), "sucesso": False}), 500

    @inject
    def atualizar(id, produto_service = Provide[Container.produto_service]):
        try:
            dados = request.get_json()
            produto_service.atualizar(id, dados)
            return jsonify({"mensagem": "Produto atualizado", "sucesso": True}), 200
        except ValueError as ve:
            return jsonify({"erro": str(ve), "sucesso": False}), 400
        except Exception as e:
            return jsonify({"erro": str(e), "sucesso": False}), 500

    @inject
    def deletar(id, produto_service = Provide[Container.produto_service]):
        try:
            produto_service.deletar(id)
            return jsonify({"mensagem": "Produto deletado", "sucesso": True}), 200
        except ValueError as ve:
            return jsonify({"erro": str(ve), "sucesso": False}), 404
        except Exception as e:
            return jsonify({"erro": str(e), "sucesso": False}), 500
