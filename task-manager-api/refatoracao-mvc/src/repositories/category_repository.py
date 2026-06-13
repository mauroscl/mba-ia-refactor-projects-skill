from src.database import db
from src.models import Category, Task
from sqlalchemy import func

class CategoryRepository:
    def get_all(self):
        return Category.query.all()

    def get_by_id(self, cat_id):
        return Category.query.get(cat_id)

    def add(self, category):
        db.session.add(category)
        db.session.commit()
        return category

    def update(self, category):
        db.session.commit()
        return category

    def delete(self, category):
        db.session.delete(category)
        db.session.commit()

    def count_all(self):
        return Category.query.count()

    def get_all_with_task_count(self):
        # N+1 Resolvido
        results = db.session.query(
            Category,
            func.count(Task.id).label('task_count')
        ).outerjoin(Task, Category.id == Task.category_id).group_by(Category.id).all()
        
        cats = []
        for cat, count in results:
            d = cat.to_dict()
            d['task_count'] = count
            cats.append(d)
        return cats
