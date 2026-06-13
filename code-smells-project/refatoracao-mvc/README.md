# E-Commerce API - Refatoração MVC

Este projeto foi refatorado para utilizar o padrão arquitetural **MVC**, **Injeção de Dependências** e **SQLAlchemy (ORM)**.

## Estrutura
O código está organizado em domínios lógicos:
- `src/models`: Modelos do banco de dados (SQLAlchemy)
- `src/repositories`: Acesso ao banco de dados isolado
- `src/services`: Regras de negócio da aplicação
- `src/controllers`: Recebem as requisições HTTP e orquestram a resposta
- `src/container.py`: Gerenciamento de injeção de dependência (`dependency-injector`)
- `app.py`: Entrypoint e roteamento

## Como executar

1. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python app.py
```

## Documentação da API
A documentação completa dos endpoints (OpenAPI 3.0) encontra-se no arquivo `openapi.yaml` localizado na raiz do projeto.
