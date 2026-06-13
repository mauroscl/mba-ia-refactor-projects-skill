# Task Manager API - Refatorada (MVC)

Aplicação refatorada aplicando o padrão arquitetural MVC, Repository Pattern, Container de Injeção de Dependências e configurações baseadas em variáveis de ambiente.

## Como Executar

1. Crie um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o ambiente:
   ```bash
   cp .env.example .env
   # Edite o .env se necessário
   ```

4. Execute a aplicação:
   ```bash
   python app.py
   ```

A API estará disponível em `http://localhost:5002`.

## Documentação

A documentação OpenAPI encontra-se no arquivo `openapi.yaml` na raiz deste projeto.
