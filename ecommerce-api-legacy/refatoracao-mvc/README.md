# E-Commerce API Refatorada

Este projeto contém a refatoração do `ecommerce-api-legacy` para o padrão MVC, utilizando **Node.js**, **Express**, **Sequelize** e **Awilix** (Injeção de Dependências).

## Principais Alterações
- Separação em camadas (`Models`, `Repositories`, `Services`, `Controllers`, `Routes`).
- Uso de `Sequelize` (ORM) para resolver explícito "Select N+1" via Eager Loading e manipulação de DB.
- Adição de `Awilix` para Container Inversion of Control (IoC).
- Extração de credenciais hardcoded para `.env`.
- Criptografia com algoritmo seguro (`bcrypt`).
- Remoção do aninhamento de blocos de callbacks (`Callback Hell`), migrando para `async/await`.
- Atualização das dependências desatualizadas para mitigação de vulnerabilidades críticas do `npm audit`.
- Geração de documentação OpenAPI 3.0 via Swagger.

## Como rodar o projeto

1. **Instale as dependências**
   ```bash
   npm install
   ```

2. **Copie o env ou rode com padrão**
   O sistema já possui um `.env` localmente configurado para banco em arquivo SQLite (`database.sqlite`).

3. **Inicie o servidor**
   ```bash
   npm start
   ```

A API estará rodando em `http://localhost:3000`.

## Documentação
Acesse a documentação gerada via Swagger em:
**http://localhost:3000/swagger-ui**
