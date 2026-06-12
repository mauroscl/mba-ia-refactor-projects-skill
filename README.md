# Analise Manual

## code-smells-project
- Secret Key hardcoded
- Secret Key retornando no endpoint de health
- apenas um controller para todos os endpoints
- todas as regras no controller
- rotas de administrador sem permissão específica.
- sem modelo de dados
- apenas uma classe (models.py) para todas as features
- senha salva sem criptografia.
- regras repetidas no criar e atualizar
- sem tratamento de sql injection
- missing imports seria um problema?

## e-commerce-api-legacy
- senha persistida sem criptografia
- nome de variáveis só com uma letra
- classe com muita responsabilidade ( AppManager.js)
- lógica toda nas rotas
- aninhamento de `if`
- exposição de credenciais de usuário e do gateway de pagamento no código.
- log de dados sensíveis: número do cartão e chave do api gateway
- tratamento de erro descentralizado
- variáveis soltas sem classes
- função declarada no meio de outro método
- muitas chamadas ao banco no endpoint do relatório. Poderia reduzir fazendo join.
- falta de controle de transação
- exclusão de usuário com matricula e pagamentos. (não deixar dados orfãos)

## task-manager-api
- uso de método deprecated `utcnow`
- toda a lógica em routes
- select n + 1 pra cada linha de tasks retornada. Poderia fazer com join
- sem mecanismo de paginação na busca de tasks, users
- lógica do cálculo do `overdue` repetida
- validações repetidas no criar e no atualizar
- muitas chamadas (6) ao banco no método `task_stats` da classe `task_routes.py`
- encode da senha na classe `user`
- encode da senha com algoritmo fraco `md5`
- senha exposta no método GET