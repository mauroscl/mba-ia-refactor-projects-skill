from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from src.container import Container

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['GET'])
@inject
def get_tasks(task_service = Provide[Container.task_service]):
    return jsonify(task_service.get_all()), 200

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
@inject
def get_task(task_id, task_service = Provide[Container.task_service]):
    try:
        return jsonify(task_service.get_by_id(task_id)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@task_bp.route('/tasks', methods=['POST'])
@inject
def create_task(task_service = Provide[Container.task_service]):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400
    try:
        task = task_service.create(data)
        return jsonify(task.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro ao criar task'}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@inject
def update_task(task_id, task_service = Provide[Container.task_service]):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400
    try:
        task = task_service.update(task_id, data)
        return jsonify(task.to_dict()), 200
    except ValueError as e:
        # Simplificação: assume que erro é ou 404 ou 400
        if 'não encontrada' in str(e) or 'não encontrado' in str(e):
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro ao atualizar'}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@inject
def delete_task(task_id, task_service = Provide[Container.task_service]):
    try:
        task_service.delete(task_id)
        return jsonify({'message': 'Task deletada com sucesso'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception:
        return jsonify({'error': 'Erro ao deletar'}), 500

@task_bp.route('/tasks/search', methods=['GET'])
@inject
def search_tasks(task_service = Provide[Container.task_service]):
    query = request.args.get('q', '')
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')
    user_id = request.args.get('user_id', '')

    results = task_service.search(query, status, priority, user_id)
    return jsonify(results), 200

@task_bp.route('/tasks/stats', methods=['GET'])
@inject
def task_stats(task_service = Provide[Container.task_service]):
    return jsonify(task_service.stats()), 200
