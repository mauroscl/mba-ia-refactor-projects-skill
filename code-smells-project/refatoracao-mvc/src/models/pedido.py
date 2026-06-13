from src.database import db
from datetime import datetime, timezone

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    status = db.Column(db.String(50), default='pendente')
    total = db.Column(db.Float, nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship to user
    usuario = db.relationship('Usuario', backref='pedidos')
    
    # Relationship to items
    itens = db.relationship('ItemPedido', backref='pedido', lazy='joined', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "status": self.status,
            "total": self.total,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "itens": [item.to_dict() for item in self.itens]
        }
