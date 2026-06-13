from src.models.produto import Produto
from src.repositories.produto_repository import ProdutoRepository

class ProdutoService:
    def __init__(self, repository: ProdutoRepository):
        self.repository = repository

    def listar(self):
        return self.repository.get_all()

    def buscar_por_id(self, produto_id):
        return self.repository.get_by_id(produto_id)

    def buscar(self, termo, categoria, preco_min, preco_max):
        return self.repository.search(termo, categoria, preco_min, preco_max)

    def criar(self, dados):
        if "nome" not in dados or "preco" not in dados or "estoque" not in dados:
            raise ValueError("Nome, preço e estoque são obrigatórios")

        if dados["preco"] < 0 or dados["estoque"] < 0:
            raise ValueError("Preço e estoque não podem ser negativos")

        categorias_validas = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]
        categoria = dados.get("categoria", "geral")
        if categoria not in categorias_validas:
            raise ValueError(f"Categoria inválida. Válidas: {categorias_validas}")

        produto = Produto(
            nome=dados["nome"],
            descricao=dados.get("descricao", ""),
            preco=dados["preco"],
            estoque=dados["estoque"],
            categoria=categoria
        )
        return self.repository.create(produto)

    def atualizar(self, produto_id, dados):
        produto = self.repository.get_by_id(produto_id)
        if not produto:
            raise ValueError("Produto não encontrado")

        if "preco" in dados and dados["preco"] < 0:
            raise ValueError("Preço não pode ser negativo")
        if "estoque" in dados and dados["estoque"] < 0:
            raise ValueError("Estoque não pode ser negativo")

        produto.nome = dados.get("nome", produto.nome)
        produto.descricao = dados.get("descricao", produto.descricao)
        produto.preco = dados.get("preco", produto.preco)
        produto.estoque = dados.get("estoque", produto.estoque)
        produto.categoria = dados.get("categoria", produto.categoria)

        return self.repository.update(produto)

    def deletar(self, produto_id):
        produto = self.repository.get_by_id(produto_id)
        if not produto:
            raise ValueError("Produto não encontrado")
        return self.repository.delete(produto)
