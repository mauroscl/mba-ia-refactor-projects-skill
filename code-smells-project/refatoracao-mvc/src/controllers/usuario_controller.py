from flask import request, jsonify
from src.container import Container
from dependency_injector.wiring import Provide, inject

class UsuarioController:
    @inject
    def listar(usuario_service = Provide[Container.usuario_service]):
        try:
            usuarios = usuario_service.listar()
            return jsonify({"dados": [u.to_dict() for u in usuarios], "sucesso": True}), 200
        except Exception as e:
            return jsonify({"erro": str(e), "sucesso": False}), 500

    @inject
    def buscar_por_id(id, usuario_service = Provide[Container.usuario_service]):
        try:
            usuario = usuario_service.buscar_por_id(id)
            if usuario:
                return jsonify({"dados": usuario.to_dict(), "sucesso": True}), 200
            return jsonify({"erro": "Usuário não encontrado", "sucesso": False}), 404
        except Exception as e:
            return jsonify({"erro": str(e), "sucesso": False}), 500

    @inject
    def criar(usuario_service = Provide[Container.usuario_service]):
        try:
            dados = request.get_json()
            usuario = usuario_service.criar(dados)
            return jsonify({"dados": {"id": usuario.id}, "mensagem": "Usuário criado", "sucesso": True}), 201
        except ValueError as ve:
            return jsonify({"erro": str(ve), "sucesso": False}), 400
        except Exception as e:
            return jsonify({"erro": str(e), "sucesso": False}), 500

    @inject
    def login(usuario_service = Provide[Container.usuario_service]):
        try:
            dados = request.get_json()
            email = dados.get("email")
            senha = dados.get("senha")
            usuario = usuario_service.login(email, senha)
            return jsonify({"dados": usuario.to_dict(), "mensagem": "Login OK", "sucesso": True}), 200
        except ValueError as ve:
            return jsonify({"erro": str(ve), "sucesso": False}), 401
        except Exception as e:
            return jsonify({"erro": str(e), "sucesso": False}), 500
