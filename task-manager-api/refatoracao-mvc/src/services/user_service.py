import re
from datetime import datetime

class UserService:
    def __init__(self, user_repository, task_repository):
        self.user_repo = user_repository
        self.task_repo = task_repository

    def get_all(self):
        users = self.user_repo.get_all()
        return [
            {**u.to_dict(), 'task_count': len(u.tasks)} for u in users
        ]

    def get_by_id(self, user_id):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError('Usuário não encontrado')
        
        data = user.to_dict()
        tasks = self.task_repo.get_by_user_id(user_id)
        data['tasks'] = [t.to_dict() for t in tasks]
        return data

    def create(self, data):
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')

        if not name: raise ValueError('Nome é obrigatório')
        if not email: raise ValueError('Email é obrigatório')
        if not password: raise ValueError('Senha é obrigatória')

        if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', email):
            raise ValueError('Email inválido')

        if len(password) < 4:
            raise ValueError('Senha deve ter no mínimo 4 caracteres')

        existing = self.user_repo.get_by_email(email)
        if existing:
            raise ValueError('Email já cadastrado')

        if role not in ['user', 'admin', 'manager']:
            raise ValueError('Role inválido')

        from src.models import User
        user = User(name=name, email=email, role=role)
        user.set_password(password)

        return self.user_repo.add(user)

    def update(self, user_id, data):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError('Usuário não encontrado')

        if 'name' in data:
            user.name = data['name']

        if 'email' in data:
            if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', data['email']):
                raise ValueError('Email inválido')
            existing = self.user_repo.get_by_email(data['email'])
            if existing and existing.id != user_id:
                raise ValueError('Email já cadastrado')
            user.email = data['email']

        if 'password' in data:
            if len(data['password']) < 4:
                raise ValueError('Senha muito curta')
            user.set_password(data['password'])

        if 'role' in data:
            if data['role'] not in ['user', 'admin', 'manager']:
                raise ValueError('Role inválido')
            user.role = data['role']

        if 'active' in data:
            user.active = data['active']

        return self.user_repo.update(user)

    def delete(self, user_id):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError('Usuário não encontrado')

        # Cascata manual das tasks
        tasks = self.task_repo.get_by_user_id(user_id)
        for t in tasks:
            self.task_repo.delete(t)

        self.user_repo.delete(user)

    def get_user_tasks(self, user_id):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError('Usuário não encontrado')

        tasks = self.task_repo.get_by_user_id(user_id)
        return [t.to_dict() for t in tasks]

    def login(self, email, password):
        if not email or not password:
            raise ValueError('Email e senha são obrigatórios')

        user = self.user_repo.get_by_email(email)
        if not user or not user.check_password(password):
            raise ValueError('Credenciais inválidas')

        if not user.active:
            raise ValueError('Usuário inativo')

        return user
