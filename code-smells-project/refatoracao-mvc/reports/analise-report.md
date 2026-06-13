================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      Python
Framework:      Flask 3.1.1
Dependência/Build: pip / requirements.txt
Dependencies:  flask==3.1.1, flask-cors==5.0.1
Domain:        E-commerce API (produtos, pedidos, usuários)
Architecture:  Monolítica — tudo centralizado em poucos arquivos, sem separação formal de camadas (Controller acessando DB/Models). Acesso ao DB utilizando raw SQL acoplado à implementação local via driver nativo (sqlite3).
Source files:  4 arquivos Python principais analisados (app.py, controllers.py, models.py, database.py)
DB tables:     produtos, usuarios, pedidos, itens_pedido
Componentes Externos:
 - Categoria: Banco de Dados
 - Ferramenta: SQLite3 (local, via arquivo loja.db)
================================