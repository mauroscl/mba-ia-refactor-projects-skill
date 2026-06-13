from src.database import db
from src.models import User, Task
from sqlalchemy import func

class UserRepository:
    def get_all(self):
        return User.query.all()

    def get_by_id(self, user_id):
        return User.query.get(user_id)

    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def add(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user):
        db.session.commit()
        return user

    def delete(self, user):
        db.session.delete(user)
        db.session.commit()

    def count_all(self):
        return User.query.count()

    def get_user_stats(self):
        # Resolvendo N+1: Agrupando as tasks por usuário em uma única consulta
        # e fazendo Left Outer Join com Users
        results = db.session.query(
            User.id,
            User.name,
            func.count(Task.id).label('total_tasks'),
            func.sum(db.case((Task.status == 'done', 1), else_=0)).label('completed_tasks')
        ).outerjoin(Task, User.id == Task.user_id).group_by(User.id, User.name).all()
        
        stats = []
        for r in results:
            total = r.total_tasks or 0
            completed = r.completed_tasks or 0
            stats.append({
                'user_id': r.id,
                'user_name': r.name,
                'total_tasks': total,
                'completed_tasks': completed,
                'completion_rate': round((completed / total) * 100, 2) if total > 0 else 0
            })
        return stats
