# Anti-pattern: Múltiplas Classes no Mesmo Arquivo e Omissão de Tipagem
**Linguagem de Exemplo:** Python

## Descrição
Declarar várias classes de domínios diferentes dentro do mesmo arquivo fonte (violando a coesão modular) e omitir as anotações de tipo (Type Hints) ou utilizar o tipo `Any`. Isso torna o código difícil de navegar, impossibilita que a IDE forneça autocompletar inteligente e mascara erros que só estourarão em tempo de execução.

## Como NÃO Fazer
```python
# Arquivo: sistema_god_file.py
# PROBLEMA 1: Classes de domínios totalmente diferentes (Cliente, Produto, Pedido) no mesmo arquivo.

class Cliente:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

class Produto:
    def __init__(self, titulo, preco):
        self.titulo = titulo
        self.preco = preco

class PedidoService:
    # PROBLEMA 2: Omissão de tipos. O que é 'cliente'? O que é 'itens'? Uma lista? Uma string?
    # PROBLEMA 3: Uso do tipo 'Any' anula as vantagens da tipagem estática moderna do Python.
    def fechar_pedido(self, cliente: any, itens, desconto) -> any:
        total = 0
        for item in itens:
            total += item.preco  # Se 'item' não for um Produto, isso gerará um AttributeError no meio da execução.
        
        total -= desconto
        print(f"Enviando recibo para {cliente.email}. Total: {total}")
        return total
```

## Como fazer corretamente

# SOLUÇÃO 1: Cada classe deve viver em seu próprio arquivo/módulo correspondente ao seu domínio.

# --- Arquivo: models/cliente.py ---
```python
class Cliente:
    def __init__(self, nome: str, email: str):
        self.nome = nome
        self.email = email
```
# --- Arquivo: models/produto.py ---
```python
class Produto:
    def __init__(self, titulo: str, preco: float):
        self.titulo = titulo
        self.preco = preco
```
# --- Arquivo: services/pedido_service.py ---
```python
from typing import List
from models.cliente import Cliente
from models.produto import Produto
class PedidoService:
    # SOLUÇÃO 2: Contratos explícitos usando Type Hints rigorosos.
    def fechar_pedido(self, cliente: Cliente, itens: List[Produto], desconto: float) -> float:
        total: float = sum(item.preco for item in itens)
        total -= desconto
        
        print(f"Enviando recibo para {cliente.email}. Total: {total}")
        return total
```

## Impacto da Refatoração
- Previsibilidade: Ferramentas de análise estática como mypy ou pyright agora conseguem analisar o código antes da execução e avisar se alguém tentar passar uma string no lugar da lista de itens.

- Navegabilidade: Localizar regras de negócio fica intuitivo. O desenvolvedor sabe exatamente em qual arquivo procurar as informações de Produto sem precisar rolar por um arquivo de 2.000 linhas.