from src.models.usuario import Usuario
from src.repositories.usuario_repository import UsuarioRepository
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def listar(self):
        return self.repository.get_all()

    def buscar_por_id(self, usuario_id):
        return self.repository.get_by_id(usuario_id)

    def criar(self, dados):
        if not dados.get("nome") or not dados.get("email") or not dados.get("senha"):
            raise ValueError("Nome, email e senha são obrigatórios")

        if self.repository.get_by_email(dados["email"]):
            raise ValueError("Email já cadastrado")

        usuario = Usuario(
            nome=dados["nome"],
            email=dados["email"],
            senha=generate_password_hash(dados["senha"]),
            tipo=dados.get("tipo", "cliente")
        )
        return self.repository.create(usuario)

    def login(self, email, senha):
        usuario = self.repository.get_by_email(email)
        if not usuario or not check_password_hash(usuario.senha, senha):
            raise ValueError("Email ou senha inválidos")
        return usuario
