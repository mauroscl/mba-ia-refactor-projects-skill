from src.models.pedido import Pedido
from src.models.item_pedido import ItemPedido
from src.repositories.pedido_repository import PedidoRepository
from src.repositories.produto_repository import ProdutoRepository
import logging

logger = logging.getLogger(__name__)

class PedidoService:
    def __init__(self, pedido_repo: PedidoRepository, produto_repo: ProdutoRepository):
        self.pedido_repo = pedido_repo
        self.produto_repo = produto_repo

    def listar_todos(self):
        return self.pedido_repo.get_all()

    def listar_por_usuario(self, usuario_id):
        return self.pedido_repo.get_by_usuario(usuario_id)

    def criar(self, dados):
        usuario_id = dados.get("usuario_id")
        itens_dados = dados.get("itens", [])

        if not usuario_id:
            raise ValueError("Usuario ID é obrigatório")
        if not itens_dados:
            raise ValueError("Pedido deve ter pelo menos 1 item")

        total = 0
        itens_pedido = []

        for item_data in itens_dados:
            produto = self.produto_repo.get_by_id(item_data["produto_id"])
            if not produto:
                raise ValueError(f"Produto {item_data['produto_id']} não encontrado")
            
            quantidade = item_data["quantidade"]
            if produto.estoque < quantidade:
                raise ValueError(f"Estoque insuficiente para {produto.nome}")

            # Desconta estoque
            produto.estoque -= quantidade
            self.produto_repo.update(produto)

            preco_unitario = produto.preco
            total += preco_unitario * quantidade

            item = ItemPedido(
                produto_id=produto.id,
                quantidade=quantidade,
                preco_unitario=preco_unitario
            )
            itens_pedido.append(item)

        pedido = Pedido(
            usuario_id=usuario_id,
            status='pendente',
            total=total,
            itens=itens_pedido
        )

        criado = self.pedido_repo.create(pedido)
        logger.info(f"Pedido {criado.id} criado. Total: {total}")
        return criado

    def atualizar_status(self, pedido_id, status):
        status_validos = ["pendente", "aprovado", "enviado", "entregue", "cancelado"]
        if status not in status_validos:
            raise ValueError("Status inválido")

        pedido = self.pedido_repo.get_by_id(pedido_id)
        if not pedido:
            raise ValueError("Pedido não encontrado")

        pedido.status = status
        
        if status == "cancelado":
            # Devolve estoque
            for item in pedido.itens:
                produto = self.produto_repo.get_by_id(item.produto_id)
                if produto:
                    produto.estoque += item.quantidade
                    self.produto_repo.update(produto)

        logger.info(f"Pedido {pedido_id} status atualizado para {status}")
        return self.pedido_repo.update(pedido)

class RelatorioService:
    def __init__(self, pedido_repo: PedidoRepository):
        self.pedido_repo = pedido_repo

    def gerar_relatorio_vendas(self):
        stats = self.pedido_repo.get_stats()
        
        faturamento = stats["faturamento"]
        desconto = 0
        if faturamento > 10000:
            desconto = faturamento * 0.1
        elif faturamento > 5000:
            desconto = faturamento * 0.05
        elif faturamento > 1000:
            desconto = faturamento * 0.02

        total_pedidos = stats["total_pedidos"]

        return {
            "total_pedidos": total_pedidos,
            "faturamento_bruto": round(faturamento, 2),
            "desconto_aplicavel": round(desconto, 2),
            "faturamento_liquido": round(faturamento - desconto, 2),
            "pedidos_pendentes": stats["pendentes"],
            "pedidos_aprovados": stats["aprovados"],
            "pedidos_cancelados": stats["cancelados"],
            "ticket_medio": round(faturamento / total_pedidos, 2) if total_pedidos > 0 else 0
        }
