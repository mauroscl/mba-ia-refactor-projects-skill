================================ 
ARCHITECTURE AUDIT REPORT  
================================  
Project: ecommerce-api-legacy
Stack:   Node.js + Express
Files:   4 analyzed

## Summary
CRITICAL: 3 | HIGH: 2 | MEDIUM: 2 | LOW: 1

## Findings

### [CRITICAL] God Class e Ausência de MVC
File: src/AppManager.js
Description: O arquivo concentra configuração do banco, definição de schema, definição de rotas e lógicas de negócio complexas (checkout, relatórios). Não há separação de responsabilidades (Controllers, Services, Models).
Impact: Manutenibilidade e testabilidade seriamente comprometidas. Qualquer alteração tem alto risco de quebrar outras partes do sistema.
Recommendation: Refatorar seguindo o padrão MVC. Separar rotas de controllers e mover a lógica de negócios e acesso a dados para services e repositories usando injeção de dependência.

### [CRITICAL] Hardcoded Credentials
File: src/utils.js:1-7
Description: Configurações sensíveis (senhas de banco de dados, chaves de API de pagamento) estão hardcoded no código fonte.
Impact: Risco crítico de vazamento de credenciais se o repositório for exposto.
Recommendation: Mover todas as credenciais para variáveis de ambiente (e.g., usando `dotenv`) e removê-las do código-fonte.

### [CRITICAL] Criptografia Fraca (Algoritmo Caseiro)
File: src/utils.js:15-21
Description: A função `badCrypto` utiliza um algoritmo inseguro baseado em múltiplas iterações de `base64` truncadas para o hash de senhas, não oferecendo nenhuma proteção real.
Impact: As senhas dos usuários podem ser facilmente quebradas.
Recommendation: Substituir por uma biblioteca padrão e segura da indústria, como `bcrypt` ou `argon2`.

### [HIGH] Vulnerabilidades nas Dependências (npm audit)
File: package.json
Description: O projeto possui dependências desatualizadas com 13 vulnerabilidades conhecidas (6 High), incluindo `sqlite3` e `express`.
Impact: Risco de Denial of Service (DoS) e acesso indevido a arquivos (Path Traversal).
Recommendation: Atualizar as dependências afetadas para versões seguras (ex: `express@5.x` ou patches mais recentes de segurança, e `sqlite3@6.x`).

### [HIGH] N+1 Queries e Aninhamento de Blocos (Callback Hell)
File: src/AppManager.js:81-125
Description: O endpoint `/api/admin/financial-report` executa queries dentro de loops (cursos -> matrículas -> usuários -> pagamentos). Além disso, o código sofre de aninhamento excessivo (Callback Hell).
Impact: Degradação severa de performance à medida que a base de dados cresce. Difícil leitura de código.
Recommendation: Utilizar um ORM/Query Builder para substituir as múltiplas queries por `JOIN`s no banco de dados e modernizar o assincronismo usando `async/await`.

### [MEDIUM] Nomes de Variáveis Sem Semântica
File: src/AppManager.js:35-39
Description: Variáveis na rota de checkout (`u`, `e`, `p`, `cid`, `cc`) não deixam claro seu propósito.
Impact: Dificulta a compreensão e manutenção do código por outros desenvolvedores.
Recommendation: Renomear as variáveis para nomes significativos (`username`, `email`, `password`, `courseId`, `creditCard`).

### [MEDIUM] Validação Fraca de Inputs
File: src/AppManager.js:41
Description: Validações básicas feitas com if inline, sem garantir o tipo ou o formato correto dos dados de entrada (ex: se o email é um email válido).
Impact: Dados inconsistentes ou errados podem ser inseridos no banco.
Recommendation: Implementar validação estruturada em nível de rotas e Models (ex: utilizando bibliotecas como `zod` ou `joi`).

### [LOW] Tratamento Genérico de Erros
File: src/AppManager.js
Description: Uso massivo de `return res.status(500).send("Erro DB")`, ocultando os verdadeiros erros e dificultando o debugging.
Impact: Dificuldade em identificar a causa raiz quando um problema acontece em produção.
Recommendation: Implementar middleware centralizado de tratamento de erros, com logs apropriados.

================================
Total: 8 findings
================================