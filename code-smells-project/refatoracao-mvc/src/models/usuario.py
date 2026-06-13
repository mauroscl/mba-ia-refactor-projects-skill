from src.database import db
from datetime import datetime, timezone

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)  # agora será hashed
    tipo = db.Column(db.String(50), default='cliente')
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "tipo": self.tipo,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None
        }
