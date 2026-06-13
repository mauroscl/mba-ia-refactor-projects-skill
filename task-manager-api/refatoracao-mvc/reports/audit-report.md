================================ 
ARCHITECTURE AUDIT REPORT  
================================  
Project: Task Manager API
Stack:   Python + Flask
Files:   ~12 analyzed

## Summary
CRITICAL: 2 | HIGH: 2 | MEDIUM: 2 | LOW: 1

## Findings

### [CRITICAL] Dados Sensíveis Hardcoded
File: app.py:12
Description: A chave `SECRET_KEY` está hardcoded em texto plano (`'super-secret-key-123'`).
Impact: Exposição da chave que assina sessões/tokens, permitindo falsificação de tokens.
Recommendation: Migrar para variável de ambiente carregada através de um módulo de configuração e `.env`.

### [CRITICAL] Credenciais Hardcoded e Senhas não Criptografadas
File: services/notification_service.py:8-9
Description: Credenciais de serviço de email (`taskmanager@gmail.com` e `senha123`) e porta SMTP declarados em texto claro.
Impact: Risco extremo de segurança se o repositório for comprometido.
Recommendation: Injetar credenciais via variáveis de ambiente.

### [HIGH] Mistura de Responsabilidades (Falta de Controllers dedicados / God Route)
File: routes/task_routes.py, routes/user_routes.py
Description: As rotas implementam a lógica de negócio completa, consultas diretas ao banco usando os Models do SQLAlchemy, validação e formatação, violando o princípio SRP.
Impact: Dificulta a testabilidade e manutenção, criando acoplamento excessivo entre requisição HTTP e lógica de negócio.
Recommendation: Refatorar movendo a lógica de negócios para a camada de Service, e mantendo os Controllers apenas para orquestração da requisição/resposta.

### [HIGH] Ausência do Padrão Repository e Container de DI
File: models/task.py, routes/*_routes.py
Description: As consultas ao banco são realizadas diretamente chamando os métodos `Model.query.*` em múltiplos arquivos. Além disso, os serviços não são injetados.
Impact: Substituição do banco de dados ou a implementação de dublês de testes fica complexa ou impossível sem mock global.
Recommendation: Criar a camada Repository para encapsular as consultas de banco de dados e utilizar um Container de Injeção de Dependência (ex: `dependency-injector` ou injeção manual estruturada).

### [MEDIUM] Select N+1 Explícito e Falta de Agregação no DB
File: routes/report_routes.py:53-56
Description: O relatório itera sobre todos os usuários (`User.query.all()`) e, para cada um, realiza uma consulta de tarefas (`Task.query.filter_by(user_id=u.id).all()`).
Impact: Queda severa de performance se a base de dados crescer.
Recommendation: Utilizar queries com `JOIN` ou agrupamento e agregação SQL na camada de Repository.

### [MEDIUM] Repetição de Código (Lógica Overdue)
File: routes/task_routes.py (várias linhas), routes/report_routes.py, routes/user_routes.py
Description: A regra que determina se uma tarefa está atrasada (passou do `due_date`, status != `done` e != `cancelled`) é replicada mais de 5 vezes no código.
Impact: Se a regra mudar, haverá inconsistências se uma das implementações for esquecida.
Recommendation: Mover o comportamento para dentro da Entidade/Model ou Serviço, implementando o princípio DRY.

### [LOW] Log de Operações Padrão no Console
File: routes/task_routes.py:102, routes/user_routes.py:64
Description: Uso de `print` livremente nas rotas em caso de sucesso ou exceção.
Impact: Falta de rastreabilidade apropriada e formatação inconsistente dos logs do servidor.
Recommendation: Utilizar o módulo `logging` nativo com o nível adequado (INFO/ERROR).

================================
Total: 7 findings
================================