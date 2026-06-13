================================ 
ARCHITECTURE AUDIT REPORT  
================================  
Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed

## Summary
CRITICAL: 3 | HIGH: 3 | MEDIUM: 1 | LOW: 1

## Findings

### [CRITICAL] SQL Injection Generalizado
- **File:** `models.py` e `app.py:53`
- **Description:** Concatenação de strings brutas para formar consultas SQL em quase todas as funções, por exemplo: `"SELECT * FROM produtos WHERE id = " + str(id)`. Em `app.py`, a rota `/admin/query` permite que o usuário envie strings SQL pela request, as quais são executadas diretamente.
- **Impact:** Controle total da base de dados por qualquer usuário mal-intencionado. Risco iminente de perda de dados, corrupção, e roubo massivo de informações confidenciais.
- **Recommendation:** Refatorar a camada de persistência para utilizar um ORM (como SQLAlchemy) e migrar para a utilização de parâmetros parametrizados na criação de queries.

### [CRITICAL] Senhas não Criptografadas e Exposição de Dados
- **File:** `controllers.py:202`, `models.py:126`, `models.py:171`
- **Description:** As senhas dos usuários estão salvas no banco de dados em texto simples (plain text). Além disso, funções como `get_todos_usuarios` e a resposta do endpoint de `login` retornam o payload completo contendo as senhas em texto puro. 
- **Impact:** Caso haja vazamento de banco de dados ou escuta em rede não segura, as senhas dos usuários estarão totalmente expostas.
- **Recommendation:** Implementar hash de senhas utilizando bibliotecas padrão de segurança (como bcrypt/werkzeug.security) e utilizar DTOs para evitar o envio de dados sensíveis para o cliente.

### [CRITICAL] Hardcoded Credentials & Segredos
- **File:** `app.py:6`, `app.py:168`
- **Description:** A variável de configuração `SECRET_KEY` está hardcoded com o valor `"minha-chave-super-secreta-123"`. Pior ainda, a rota `/health` em `app.py` expõe essa mesma chave num JSON de resposta para qualquer usuário que acessar a URL.
- **Impact:** A chave exposta pode ser utilizada para falsificar sessões e manipular tokens, comprometendo completamente a segurança do app.
- **Recommendation:** Carregar configurações de segurança via variáveis de ambiente utilizando pacotes como `python-dotenv` ou `os.getenv`, e remover as credenciais/segredos das respostas da API.

### [HIGH] Ausência de Arquitetura em Camadas (Falta MVC, DI e SRP)
- **File:** `models.py`, `controllers.py`
- **Description:** `models.py` é uma God Class que engloba queries brutas, validação de itens de pedidos e agregação. O `controllers.py` mistura requisições HTTP com lógicas de negócio pesadas (verificação de categorias e preços) e notificação por prints (Email, SMS, Push). Não existe padrão Repository, nem injeção de dependência.
- **Impact:** Dificuldade acentuada de manutenção, repetição de código e testes de unidade quase inviáveis devido ao alto acoplamento e dependência oculta de banco de dados e objetos de request.
- **Recommendation:** Refatorar o projeto para o padrão MVC, criando camadas independentes: `Routes`, `Controllers`, `Services`, e `Repositories`, interligados via Injeção de Dependência (utilizando `dependency-injector` ou injeção clássica via construtor/factory).

### [HIGH] SELECT N+1 Explícito e Implícito
- **File:** `models.py:214` (`get_pedidos_usuario`), `models.py:246` (`get_todos_pedidos`)
- **Description:** Para carregar os itens associados a cada pedido de usuário, as funções executam a iteração 1 a 1: loop de pedidos faz query na tabela `itens_pedido`, e outro loop executa query na tabela `produtos` para buscar nomes.
- **Impact:** Perda grave de performance. Essa estrutura fará $1 + N + (N \times M)$ consultas no banco, podendo levar à queda do banco de dados na presença de tráfego real.
- **Recommendation:** Utilizar a capacidade de Join/Eager Loading de um ORM para realizar as consultas agrupadas.

### [HIGH] God Files / Mistura de Domínios
- **File:** `app.py`, `controllers.py`, `models.py`
- **Description:** O projeto não separa os arquivos por domínio do problema. Produtos, pedidos, relatórios e usuários estão todos agrupados e entrelaçados no mesmo arquivo.
- **Impact:** Muito complexo de escalar o time de desenvolvimento; alterações em "produto" podem inadvertidamente quebrar "usuário" devido a conflitos de merge ou escopo global no banco.
- **Recommendation:** Separar cada domínio de negócio em sua própria pasta com seus respectivos Controllers, Services e Repositories (`src/domains/produto`, `src/domains/pedido`, etc).

### [MEDIUM] Lógica de Negócio Espalhada
- **File:** `controllers.py:228`
- **Description:** A validação para criar pedido, descontar o estoque, notificar por e-mail, entre outros, está misturada na rota e nas models.
- **Impact:** Violação do padrão arquitetural e SRP.
- **Recommendation:** Movimentar todas essas validações para um Caso de Uso ou Service (ex: `CriarPedidoService`).

### [LOW] Magic Strings e Prints em Produção
- **File:** Múltiplos
- **Description:** Presença de `"pendente"`, `"aprovado"` hardcoded pelo código. Uso excessivo de `print` ao invés de um sistema de log padrão (`logging`).
- **Impact:** Propensão a erros de digitação e impossibilidade de monitorar adequadamente logs em produção.
- **Recommendation:** Introduzir o módulo `logging` padrão do Python e utilizar `Enum` para os status e categorias.

================================
