from src.database import db
from src.models.pedido import Pedido
from sqlalchemy import func

class PedidoRepository:
    def get_all(self):
        return Pedido.query.all()

    def get_by_usuario(self, usuario_id):
        return Pedido.query.filter_by(usuario_id=usuario_id).all()

    def get_by_id(self, pedido_id):
        return Pedido.query.get(pedido_id)

    def create(self, pedido: Pedido):
        db.session.add(pedido)
        db.session.commit()
        return pedido

    def update(self, pedido: Pedido):
        db.session.commit()
        return pedido

    def get_stats(self):
        total_pedidos = db.session.query(func.count(Pedido.id)).scalar() or 0
        faturamento = db.session.query(func.sum(Pedido.total)).scalar() or 0
        pendentes = db.session.query(func.count(Pedido.id)).filter_by(status='pendente').scalar() or 0
        aprovados = db.session.query(func.count(Pedido.id)).filter_by(status='aprovado').scalar() or 0
        cancelados = db.session.query(func.count(Pedido.id)).filter_by(status='cancelado').scalar() or 0

        return {
            "total_pedidos": total_pedidos,
            "faturamento": faturamento,
            "pendentes": pendentes,
            "aprovados": aprovados,
            "cancelados": cancelados
        }
