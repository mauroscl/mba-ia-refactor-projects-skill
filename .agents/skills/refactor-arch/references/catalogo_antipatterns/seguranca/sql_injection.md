# Anti-pattern: SQL Injection
**Linguagem de Exemplo:** Python

## Descrição
Construir queries SQL dinâmicas concatenando ou interpolando diretamente inputs fornecidos pelo usuário. Isso permite que comandos SQL arbitrários sejam injetados e executados pelo interpretador do banco de dados.

## Como NÃO Fazer
```python
import psycopg2

def obter_usuario_por_email(connection, user_email):
    cursor = connection.cursor()
    # PROBLEMA: Interpolação direta de strings viabiliza injeção SQL total
    query = f"SELECT id, nome, email FROM usuarios WHERE email = '{user_email}'"
    cursor.execute(query)
    return cursor.fetchone()
```

## Como Fazer Corretamente
```python
import psycopg2

def obter_usuario_por_email(connection, user_email):
    cursor = connection.cursor()
    # SOLUÇÃO: Utilização estrita de consultas parametrizadas (placeholders)
    query = "SELECT id, nome, email FROM usuarios WHERE email = %s"
    
    # O driver de banco de dados faz o escape seguro do dado, tratando-o apenas como literal
    cursor.execute(query, (user_email,))
    return cursor.fetchone()
```
## Impacto da Refatoração
- Proteção Absoluta: Neutraliza a entrada maliciosa do usuário, impossibilitando a manipulação da estrutura sintática da query.
