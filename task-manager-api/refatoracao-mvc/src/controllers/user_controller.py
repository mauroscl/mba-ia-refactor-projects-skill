from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from src.container import Container

user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['GET'])
@inject
def get_users(user_service = Provide[Container.user_service]):
    return jsonify(user_service.get_all()), 200

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@inject
def get_user(user_id, user_service = Provide[Container.user_service]):
    try:
        return jsonify(user_service.get_by_id(user_id)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@user_bp.route('/users', methods=['POST'])
@inject
def create_user(user_service = Provide[Container.user_service]):
    data = request.get_json()
    if not data: return jsonify({'error': 'Dados inválidos'}), 400
    try:
        user = user_service.create(data)
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        if 'já cadastrado' in str(e):
            return jsonify({'error': str(e)}), 409
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro ao criar usuário'}), 500

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@inject
def update_user(user_id, user_service = Provide[Container.user_service]):
    data = request.get_json()
    if not data: return jsonify({'error': 'Dados inválidos'}), 400
    try:
        user = user_service.update(user_id, data)
        return jsonify(user.to_dict()), 200
    except ValueError as e:
        if 'já cadastrado' in str(e):
            return jsonify({'error': str(e)}), 409
        if 'não encontrado' in str(e):
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 400
    except Exception:
        return jsonify({'error': 'Erro ao atualizar'}), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@inject
def delete_user(user_id, user_service = Provide[Container.user_service]):
    try:
        user_service.delete(user_id)
        return jsonify({'message': 'Usuário deletado com sucesso'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception:
        return jsonify({'error': 'Erro ao deletar'}), 500

@user_bp.route('/users/<int:user_id>/tasks', methods=['GET'])
@inject
def get_user_tasks(user_id, user_service = Provide[Container.user_service]):
    try:
        return jsonify(user_service.get_user_tasks(user_id)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@user_bp.route('/login', methods=['POST'])
@inject
def login(user_service = Provide[Container.user_service]):
    data = request.get_json()
    if not data: return jsonify({'error': 'Dados inválidos'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    try:
        user = user_service.login(email, password)
        return jsonify({
            'message': 'Login realizado com sucesso',
            'user': user.to_dict(),
            'token': 'fake-jwt-token-' + str(user.id)
        }), 200
    except ValueError as e:
        if 'inativo' in str(e):
            return jsonify({'error': str(e)}), 403
        return jsonify({'error': str(e)}), 401
