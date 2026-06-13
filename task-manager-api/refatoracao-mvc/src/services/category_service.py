class CategoryService:
    def __init__(self, category_repository):
        self.category_repo = category_repository

    def get_all(self):
        return self.category_repo.get_all_with_task_count()

    def create(self, data):
        name = data.get('name')
        if not name: raise ValueError('Nome é obrigatório')

        from src.models import Category
        category = Category(
            name=name,
            description=data.get('description', ''),
            color=data.get('color', '#000000')
        )
        return self.category_repo.add(category).to_dict()

    def update(self, cat_id, data):
        cat = self.category_repo.get_by_id(cat_id)
        if not cat: raise ValueError('Categoria não encontrada')

        if 'name' in data: cat.name = data['name']
        if 'description' in data: cat.description = data['description']
        if 'color' in data: cat.color = data['color']

        return self.category_repo.update(cat).to_dict()

    def delete(self, cat_id):
        cat = self.category_repo.get_by_id(cat_id)
        if not cat: raise ValueError('Categoria não encontrada')
        self.category_repo.delete(cat)
