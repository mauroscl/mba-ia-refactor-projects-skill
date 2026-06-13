from src.database import db
from src.models import Task

class TaskRepository:
    def get_all(self):
        return Task.query.all()

    def get_by_id(self, task_id):
        return Task.query.get(task_id)

    def get_by_user_id(self, user_id):
        return Task.query.filter_by(user_id=user_id).all()

    def count_all(self):
        return Task.query.count()

    def count_by_status(self, status):
        return Task.query.filter_by(status=status).count()

    def count_by_priority(self, priority):
        return Task.query.filter_by(priority=priority).count()

    def add(self, task):
        db.session.add(task)
        db.session.commit()
        return task

    def update(self, task):
        db.session.commit()
        return task

    def delete(self, task):
        db.session.delete(task)
        db.session.commit()

    def search(self, query=None, status=None, priority=None, user_id=None):
        tasks = Task.query
        if query:
            tasks = tasks.filter(
                db.or_(
                    Task.title.like(f'%{query}%'),
                    Task.description.like(f'%{query}%')
                )
            )
        if status:
            tasks = tasks.filter(Task.status == status)
        if priority:
            tasks = tasks.filter(Task.priority == int(priority))
        if user_id:
            tasks = tasks.filter(Task.user_id == int(user_id))
        return tasks.all()

    def get_recent_tasks_count(self, since):
        return Task.query.filter(Task.created_at >= since).count()

    def get_recent_done_count(self, since):
        return Task.query.filter(Task.status == 'done', Task.updated_at >= since).count()
