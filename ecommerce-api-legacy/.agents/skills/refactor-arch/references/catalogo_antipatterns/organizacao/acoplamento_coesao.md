# Anti-pattern: Alto Acoplamento e Baixa Coesão
**Linguagem de Exemplo:** Python

## Descrição
Baixa coesão ocorre quando uma classe mistura comportamentos sem qualquer afinidade funcional. Alto acoplamento ocorre quando uma classe conhece intimamente detalhes privados de implementação de outra, gerando um efeito dominó onde qualquer alteração quebra múltiplos arquivos.

## Como náo fazer

```python

class UtilitarioGeralDoSistema:
    # PROBLEMA: Baixa coesão (mistura formatação de texto com envio de SMS e relatórios)
    def formatar_moeda(self, valor):
        return f"R$ {valor:,.2f}"
        
    def enviar_sms_confirmacao(self, telefone, mensagem):
        print(f"Enviando SMS para {telefone}: {mensagem}")
        
    def exportar_excel_usuarios(self, lista_usuarios):
        print("Gerando planilha Excel de auditoria...")

class ProcessadorDePedidos:
    def __init__(self):
        self.utils = UtilitarioGeralDoSistema()

    def fechar_pedido(self, pedido, usuario):
        # PROBLEMA: Alto acoplamento (depende de dados brutos e muta diretamente o estado interno do pedido)
        if pedido.status == "PENDENTE":
            pedido.status = "CONCLUIDO"
            pedido.dados_internos_banco["data_modificacao"] = "2026-06-08"
            
            msg = f"Pedido {pedido.id} fechado com sucesso."
            self.utils.enviar_sms_confirmacao(usuario.telefone, msg)
```


## Como fazer corretamente

```python
# SOLUÇÃO: Criação de classes altamente coesas e desacopladas por abstração de interface ou chamadas encapsuladas

class ConversorMoeda:
    @static_method
    def para_real(valor: float) -> str:
        return f"R$ {valor:,.2f}"

class SmsNotificationService:
    def enviar_notificacao(self, telefone: str, mensagem: str) -> None:
        print(f"Enviando SMS para {telefone}: {mensagem}")

class Pedido:
    def __init__(self, pedido_id: int, status_inicial: str):
        self._id = pedido_id
        self._status = status_inicial
        self._data_modificacao = None

    @property
    def id(self):
        return self._id

    # O próprio objeto gerencia sua mutação de estado interna protegendo suas regras
    def marcar_como_concluido(self, data_atual: str) -> None:
        if self._status != "PENDENTE":
            raise ValueError("Apenas pedidos pendentes podem ser concluídos.")
        self._status = "CONCLUIDO"
        self._data_modificacao = data_atual

class ProcessadorDePedidosRefatorado:
    def __init__(self, sms_service: SmsNotificationService):
        self._sms_service = sms_service

    def fechar_pedido(self, pedido: Pedido, usuario) -> None:
        pedido.marcar_como_concluido("2026-06-08")
        
        mensagem = f"Pedido {pedido.id} fechado com sucesso."
        self._sms_service.enviar_notificacao(usuario.telefone, mensagem)

```

## Impacto da Refatoração
- Independência Coesa: Alterar o provider de SMS não afeta a classe ConversorMoeda nem quebra a lógica de pedidos.

- Blindagem Sólida: O `ProcessadorDePedidos` não manipula mais chaves brutas de dicionários de banco da classe `Pedido`.