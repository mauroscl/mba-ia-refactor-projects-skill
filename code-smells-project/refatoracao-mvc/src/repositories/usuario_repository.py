from src.database import db
from src.models.usuario import Usuario

class UsuarioRepository:
    def get_all(self):
        return Usuario.query.all()

    def get_by_id(self, usuario_id):
        return Usuario.query.get(usuario_id)

    def get_by_email(self, email):
        return Usuario.query.filter_by(email=email).first()

    def create(self, usuario: Usuario):
        db.session.add(usuario)
        db.session.commit()
        return usuario
