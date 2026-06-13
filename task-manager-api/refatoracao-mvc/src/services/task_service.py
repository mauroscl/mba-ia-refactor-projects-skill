from datetime import datetime

class TaskService:
    def __init__(self, task_repository, user_repository, category_repository, notification_service=None):
        self.task_repo = task_repository
        self.user_repo = user_repository
        self.category_repo = category_repository
        self.notification_service = notification_service

    def get_all(self):
        tasks = self.task_repo.get_all()
        result = []
        for t in tasks:
            task_data = t.to_dict()
            task_data['user_name'] = t.user.name if t.user else None
            task_data['category_name'] = t.category.name if t.category else None
            result.append(task_data)
        return result

    def get_by_id(self, task_id):
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise ValueError('Task não encontrada')
        return task.to_dict()

    def create(self, data):
        title = data.get('title')
        if not title: raise ValueError('Título é obrigatório')
        if len(title) < 3: raise ValueError('Título muito curto')
        if len(title) > 200: raise ValueError('Título muito longo')

        status = data.get('status', 'pending')
        priority = data.get('priority', 3)
        user_id = data.get('user_id')
        category_id = data.get('category_id')
        due_date = data.get('due_date')
        tags = data.get('tags')

        if status not in ['pending', 'in_progress', 'done', 'cancelled']:
            raise ValueError('Status inválido')

        if priority < 1 or priority > 5:
            raise ValueError('Prioridade deve ser entre 1 e 5')

        user = None
        if user_id:
            user = self.user_repo.get_by_id(user_id)
            if not user: raise ValueError('Usuário não encontrado')

        if category_id:
            cat = self.category_repo.get_by_id(category_id)
            if not cat: raise ValueError('Categoria não encontrada')

        from src.models import Task
        task = Task(
            title=title,
            description=data.get('description', ''),
            status=status,
            priority=priority,
            user_id=user_id,
            category_id=category_id
        )

        if due_date:
            try:
                task.due_date = datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Formato de data inválido. Use YYYY-MM-DD')

        if tags:
            task.tags = ','.join(tags) if isinstance(tags, list) else tags

        saved_task = self.task_repo.add(task)

        if user and self.notification_service:
            self.notification_service.notify_task_assigned(user, saved_task)

        return saved_task

    def update(self, task_id, data):
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise ValueError('Task não encontrada')

        if 'title' in data:
            if len(data['title']) < 3: raise ValueError('Título muito curto')
            if len(data['title']) > 200: raise ValueError('Título muito longo')
            task.title = data['title']

        if 'description' in data:
            task.description = data['description']

        if 'status' in data:
            if data['status'] not in ['pending', 'in_progress', 'done', 'cancelled']:
                raise ValueError('Status inválido')
            task.status = data['status']

        if 'priority' in data:
            if data['priority'] < 1 or data['priority'] > 5:
                raise ValueError('Prioridade deve ser entre 1 e 5')
            task.priority = data['priority']

        if 'user_id' in data:
            if data['user_id']:
                if not self.user_repo.get_by_id(data['user_id']):
                    raise ValueError('Usuário não encontrado')
            task.user_id = data['user_id']

        if 'category_id' in data:
            if data['category_id']:
                if not self.category_repo.get_by_id(data['category_id']):
                    raise ValueError('Categoria não encontrada')
            task.category_id = data['category_id']

        if 'due_date' in data:
            if data['due_date']:
                try:
                    task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Formato de data inválido')
            else:
                task.due_date = None

        if 'tags' in data:
            task.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']

        task.updated_at = datetime.utcnow()
        return self.task_repo.update(task)

    def delete(self, task_id):
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise ValueError('Task não encontrada')
        self.task_repo.delete(task)

    def search(self, query, status, priority, user_id):
        tasks = self.task_repo.search(query, status, priority, user_id)
        return [t.to_dict() for t in tasks]

    def stats(self):
        total = self.task_repo.count_all()
        pending = self.task_repo.count_by_status('pending')
        in_progress = self.task_repo.count_by_status('in_progress')
        done = self.task_repo.count_by_status('done')
        cancelled = self.task_repo.count_by_status('cancelled')

        all_tasks = self.task_repo.get_all()
        overdue_count = sum(1 for t in all_tasks if t.is_overdue())

        return {
            'total': total,
            'pending': pending,
            'in_progress': in_progress,
            'done': done,
            'cancelled': cancelled,
            'overdue': overdue_count,
            'completion_rate': round((done / total) * 100, 2) if total > 0 else 0
        }
