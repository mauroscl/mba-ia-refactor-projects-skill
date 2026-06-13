from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from src.container import Container

report_bp = Blueprint('reports', __name__)

@report_bp.route('/reports/summary', methods=['GET'])
@inject
def summary_report(report_service = Provide[Container.report_service]):
    return jsonify(report_service.generate_summary()), 200

@report_bp.route('/reports/user/<int:user_id>', methods=['GET'])
@inject
def user_report(user_id, report_service = Provide[Container.report_service]):
    try:
        return jsonify(report_service.user_report(user_id)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@report_bp.route('/categories', methods=['GET'])
@inject
def get_categories(category_service = Provide[Container.category_service]):
    return jsonify(category_service.get_all()), 200

@report_bp.route('/categories', methods=['POST'])
@inject
def create_category(category_service = Provide[Container.category_service]):
    data = request.get_json()
    if not data: return jsonify({'error': 'Dados inválidos'}), 400
    try:
        cat = category_service.create(data)
        return jsonify(cat), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception:
        return jsonify({'error': 'Erro ao criar categoria'}), 500

@report_bp.route('/categories/<int:cat_id>', methods=['PUT'])
@inject
def update_category(cat_id, category_service = Provide[Container.category_service]):
    data = request.get_json()
    if not data: return jsonify({'error': 'Dados inválidos'}), 400
    try:
        cat = category_service.update(cat_id, data)
        return jsonify(cat), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception:
        return jsonify({'error': 'Erro ao atualizar'}), 500

@report_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
@inject
def delete_category(cat_id, category_service = Provide[Container.category_service]):
    try:
        category_service.delete(cat_id)
        return jsonify({'message': 'Categoria deletada'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception:
        return jsonify({'error': 'Erro ao deletar'}), 500
