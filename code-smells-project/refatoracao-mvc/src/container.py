from dependency_injector import containers, providers
from src.repositories.produto_repository import ProdutoRepository
from src.repositories.usuario_repository import UsuarioRepository
from src.repositories.pedido_repository import PedidoRepository

from src.services.produto_service import ProdutoService
from src.services.usuario_service import UsuarioService
from src.services.pedido_service import PedidoService, RelatorioService

class Container(containers.DeclarativeContainer):
    
    # Repositories
    produto_repository = providers.Factory(ProdutoRepository)
    usuario_repository = providers.Factory(UsuarioRepository)
    pedido_repository = providers.Factory(PedidoRepository)
    
    # Services
    produto_service = providers.Factory(
        ProdutoService,
        repository=produto_repository
    )
    
    usuario_service = providers.Factory(
        UsuarioService,
        repository=usuario_repository
    )
    
    pedido_service = providers.Factory(
        PedidoService,
        pedido_repo=pedido_repository,
        produto_repo=produto_repository
    )
    
    relatorio_service = providers.Factory(
        RelatorioService,
        pedido_repo=pedido_repository
    )
