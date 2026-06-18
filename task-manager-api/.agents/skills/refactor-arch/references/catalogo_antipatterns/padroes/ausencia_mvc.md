# Anti-pattern: Ausência de MVC
**Linguagem de Exemplo:** Python

## Como NÃO Fazer
```python
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route("/usuario/<int:id_usuario>", methods=["GET"])
def visualizar_usuario(id_usuario):
    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, role FROM users WHERE id = ?", (id_usuario,))
    user = cursor.fetchone()
    
    if not user:
        return "<h1>Erro</h1><p>Usuário Não Encontrado</p>", 404
        
    html_response = f"<div><h1>Perfil: {user[0]}</h1><p>Email: {user[1]}</p></div>"
    return html_response
```

## Como Fazer Corretamente
```python
class UserModel:
    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role

    @classmethod
    def buscar_por_id(cls, user_id: int):
        if user_id == 1:
            return cls("Mauro", "mauro@empresa.com", "admin")
        return None

class UserHtmlView:
    @staticmethod
    def renderizar_detalhes(user: UserModel) -> str:
        return f"<div><h1>Perfil: {user.name}</h1><p>Email: {user.email}</p></div>"

    @staticmethod
    def renderizar_erro_nao_encontrado() -> str:
        return "<h1>Erro</h1><p>Usuário Não Encontrado</p>"

@app.route("/usuario/<int:id_usuario>", methods=["GET"])
def visualizar_usuario_controller(id_usuario):
    user = UserModel.buscar_por_id(id_usuario)
    if not user:
        return UserHtmlView.renderizar_erro_nao_encontrado(), 404
        
    return UserHtmlView.renderizar_detalhes(user), 200
```