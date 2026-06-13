from src.database import db
from src.models.produto import Produto

class ProdutoRepository:
    def get_all(self):
        return Produto.query.all()

    def get_by_id(self, produto_id):
        return Produto.query.get(produto_id)

    def search(self, termo, categoria=None, preco_min=None, preco_max=None):
        query = Produto.query
        if termo:
            query = query.filter((Produto.nome.ilike(f'%{termo}%')) | (Produto.descricao.ilike(f'%{termo}%')))
        if categoria:
            query = query.filter_by(categoria=categoria)
        if preco_min is not None:
            query = query.filter(Produto.preco >= preco_min)
        if preco_max is not None:
            query = query.filter(Produto.preco <= preco_max)
        return query.all()

    def create(self, produto: Produto):
        db.session.add(produto)
        db.session.commit()
        return produto

    def update(self, produto: Produto):
        db.session.commit()
        return produto

    def delete(self, produto: Produto):
        db.session.delete(produto)
        db.session.commit()
        return True
