from src.database import db
from datetime import datetime, timezone

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    ativo = db.Column(db.Integer, default=1)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "estoque": self.estoque,
            "categoria": self.categoria,
            "ativo": self.ativo,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None
        }
