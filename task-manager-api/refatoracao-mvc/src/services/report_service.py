from datetime import datetime, timedelta

class ReportService:
    def __init__(self, task_repository, user_repository, category_repository):
        self.task_repo = task_repository
        self.user_repo = user_repository
        self.category_repo = category_repository

    def generate_summary(self):
        total_tasks = self.task_repo.count_all()
        total_users = self.user_repo.count_all()
        total_categories = self.category_repo.count_all()

        pending = self.task_repo.count_by_status('pending')
        in_progress = self.task_repo.count_by_status('in_progress')
        done = self.task_repo.count_by_status('done')
        cancelled = self.task_repo.count_by_status('cancelled')

        p1 = self.task_repo.count_by_priority(1)
        p2 = self.task_repo.count_by_priority(2)
        p3 = self.task_repo.count_by_priority(3)
        p4 = self.task_repo.count_by_priority(4)
        p5 = self.task_repo.count_by_priority(5)

        all_tasks = self.task_repo.get_all()
        overdue_list = [
            {
                'id': t.id,
                'title': t.title,
                'due_date': str(t.due_date),
                'days_overdue': (datetime.utcnow() - t.due_date).days
            }
            for t in all_tasks if t.is_overdue()
        ]

        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_tasks = self.task_repo.get_recent_tasks_count(seven_days_ago)
        recent_done = self.task_repo.get_recent_done_count(seven_days_ago)

        user_stats = self.user_repo.get_user_stats()

        return {
            'generated_at': str(datetime.utcnow()),
            'overview': {
                'total_tasks': total_tasks,
                'total_users': total_users,
                'total_categories': total_categories,
            },
            'tasks_by_status': {
                'pending': pending,
                'in_progress': in_progress,
                'done': done,
                'cancelled': cancelled,
            },
            'tasks_by_priority': {
                'critical': p1,
                'high': p2,
                'medium': p3,
                'low': p4,
                'minimal': p5,
            },
            'overdue': {
                'count': len(overdue_list),
                'tasks': overdue_list,
            },
            'recent_activity': {
                'tasks_created_last_7_days': recent_tasks,
                'tasks_completed_last_7_days': recent_done,
            },
            'user_productivity': user_stats,
        }

    def user_report(self, user_id):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError('Usuário não encontrado')

        tasks = self.task_repo.get_by_user_id(user_id)

        total = len(tasks)
        done = sum(1 for t in tasks if t.status == 'done')
        pending = sum(1 for t in tasks if t.status == 'pending')
        in_progress = sum(1 for t in tasks if t.status == 'in_progress')
        cancelled = sum(1 for t in tasks if t.status == 'cancelled')
        high_priority = sum(1 for t in tasks if t.priority <= 2)
        overdue = sum(1 for t in tasks if t.is_overdue())

        return {
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
            },
            'statistics': {
                'total_tasks': total,
                'done': done,
                'pending': pending,
                'in_progress': in_progress,
                'cancelled': cancelled,
                'overdue': overdue,
                'high_priority': high_priority,
                'completion_rate': round((done / total) * 100, 2) if total > 0 else 0
            }
        }
