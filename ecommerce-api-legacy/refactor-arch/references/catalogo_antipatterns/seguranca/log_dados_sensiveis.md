# Anti-pattern: Log de Dados Sensíveis
**Linguagem de Exemplo:** Python

## Descrição
Gravar dados confidenciais diretamente em arquivos de logs rotineiros da aplicação (como senhas, números de cartão de crédito e tokens). Analistas e ferramentas de monitoramento têm acesso a esses arquivos, o que viola regras de conformidade como a LGPD/GDPR e a PCI-DSS.

## Como NÃO Fazer
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PaymentController")

def process_payment_request(request_data):
    # PROBLEMA: Gravando o payload inteiro que contém o número e o código de segurança do cartão
    logger.info(f"Processando requisição de pagamento recebida: {request_data}")
    
    # Executa a chamada do gateway...
    return {"status": "success"}
```

## Como Fazer Corretamente
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PaymentController")

def sanitize_payment_data(data: dict) -> dict:
    # SOLUÇÃO: Ofuscação ativa de dados críticos antes de encaminhar para o log
    sanitized = data.copy()
    if "card_number" in sanitized:
        raw_card = str(sanitized["card_number"])
        sanitized["card_number"] = f"XXXX-XXXX-XXXX-{raw_card[-4:]}" if len(raw_card) >= 4 else "XXXX"
    if "cvv" in sanitized:
        sanitized["cvv"] = "***"
    return sanitized

def process_payment_request(request_data):
    # Loga apenas o conteúdo já limpo e sanitizado
    safe_data = sanitize_payment_data(request_data)
    logger.info(f"Processando requisição de pagamento para o cliente: {safe_data.get('user_id')} - Dados: {safe_data}")
    
    # Executa a chamada do gateway...
    return {"status": "success"}
```

## Impacto da Refatoração
- Conformidade: Garante conformidade técnica com normas regulatórias e auditorias de segurança.

- Vazamento de Dados: Protege o sistema contra acessos indevidos aos servidores de centralização de logs (ex: ELK Stack, CloudWatch).