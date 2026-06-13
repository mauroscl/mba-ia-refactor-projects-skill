---
name: refactor-arch
description:
  Analisa um projeto e gera um relatório de críticas classificadas de acordo com critérios de severidade. Resolve as críticas encontradas e transforma o projeto para o padrão MVC caso ainda não utilize este padrão e seja aplicável à linguagem e ao framework do projeto.
  Use quando precisar analisar um projeto em qualquer linguagem e stack de desenvolvimento e quiser garantir que o projeto siga boas práticas de engenharia, não tenha questões de segurança e utilize a arquitetura MVC.
metadata:
  version: "1.0"
  supported_parameters:
    - path:
        type: string
        required: false
        default: "."
        description: "O caminho relativo do projeto a ser refatorado. Se omitido, usa a raiz atual."
    - mode:
        type: string
        required: false
        default: "sandbox"
        description: "Valores aceitos: 'sandbox' (cria pasta isolada intacta) ou 'inplace' (substitui os arquivos originais)."
---

# Resolução de Caminho (path) e Modo de Gravação (mode)

- Identifique os parâmetros `path` e `mode`.
  - Se `mode` for igual a `sandbox` (padrão): 
      * Crie uma nova pasta chamada `refatoracao-mvc/` dentro do diretório especificado em `path`. 
      * Toda a nova estrutura deve ser gerada **dentro** desta pasta de teste, mantendo todos os arquivos originais fora dela totalmente intocados.
  - Se `mode` for igual a `inplace`: 
      * Modifique e mova os arquivos diretamente no diretório original estabelecido em `path`.

Com o `path` definido, crie o diretório `reports` dentro do escopo de execução escolhido: em `refatoracao-mvc/reports` quando `mode` for `sandbox`, ou em `{path/reports}` quando `mode` for `inplace`. Este diretório será usado nas proximas fases.

# Instruções para o Agente Refactor-Arch

**Persona**: Você deve atuar como um Engenheiro de Software especialista em análise e refatoração de aplicações. Você é especialista no padrão MVC independente da linguagem / stack de desenvolvimento.

Seu trabalho deve ser dividido em três fases:

1. **Analise**: Descobrir stack, frameworks, ferramentas de build e arquitetura utilizada. Siga "Fase 1: Instruções de analise do projeto" abaixo.
2. **Auditoria**: Analisar o projeto e gerar um relatório de críticas classificadas de acordo com critérios de severidade (CRITICAL, HIGH, MEDIUM, LOW). Siga "Fase 2: Instruções do relatório de auditoria" abaixo.
3. **Refatoração**: Resolver as críticas encontradas na fase 2 e transfomar o projeto no padrão arquitetural MVC, caso ainda não utilize. Siga as "Fase 3: Instruções de refatoração do projeto" abaixo.

## Fase 1: Instruções de analise do projeto

Para gerar o report de análise, utilize o template [análise projeto](assets/analise-projeto-template.md) e grave no caminho `reports/analise-report.md`

Faça uma análise completa dos arquivos e estruturas de diretórios. Caso a estrutura não seja de um projeto de desenvolvimento de software pare e retorne "Não foi possivel analisar o projeto". Caso contrário prossiga.

Faça uma análise completa do projeto incluindo:

- linguagem e framework utilizados
- ferramenta de build (ex: maven, gradle, npm, pip, etc)
- dominio do problema
- comunicação com componentes externos como banco de dados, mensageria, cache, outros serviços
- dependencias
- arquitetura
- quantidade de arquivos analisados

Para cada comunicação com componentes externo indique detalhes como categoria, ferramenta utilizada, principalmente itens da ferramenta.
Exemplo para banco de dados:

- Categoria: Banco de Dados
- Servidor: Oracle, Mongo, Sql Server, etc
- Tabelas ou coleções utilizadas

Se for relevante para entender o projeto, inclua outras informações.

### Checklist de Validação

- [ ] Linguagem detectada corretamente
- [ ] Framework detectado corretamente
- [ ] Domínio da aplicação descrito corretamente
- [ ] Ferramenta de build detectada corretamente

**Ponto de DECISÃO**: Caso linguagem e framework detectaos não possuam um ecossistema amigável ao padrão MVC tradicional (ex: linguagens de script curtos ou funcionais puros), não prossiga para a fase 2, informando a razão de não continuar.

------

## Fase 2: Instruções do relatório de auditoria
- O relatório deve ser gerado no path `reports/audit-report.md`.
- O relatório deve ter o formato do [template](assets/audit-report-template.md)
- Os findings devem ser ordenados por severidade (CRITICAL → LOW)

### Definição de Severidades

- **CRITICAL:** Falhas graves de arquitetura ou segurança que impedem o funcionamento correto, expõem dados sensíveis (ex: credenciais hardcoded, SQL Injection) ou violam completamente a separação de responsabilidades (ex: "God Class" contendo banco de dados, lógicas complexas e roteamento no mesmo arquivo).
- **HIGH:** Fortes violações do padrão MVC ou princípios SOLID que dificultam muito a manutenção e testes (ex: lógicas de negócio pesadas presas dentro de Controllers, forte acoplamento sem Injeção de Dependência, ou uso de estado global mutável em toda a aplicação).
- **MEDIUM:** Problemas de padronização, duplicação de código ou gargalos de performance moderada (ex: Queries N+1 no banco de dados, uso inadequado de middlewares, validações ausentes nas rotas).
- **LOW:** Melhorias de legibilidade, nomenclatura de variáveis ruins, ou "magic numbers" soltos pelo código.

### Coleta de findings dinâmicos (Vulnerabilidades e Depreciações)

Antes de analisar o código-fonte estaticamente, você deve inspecionar o estado das dependências e APIs utilizando as ferramentas nativas do ecossistema do projeto. Execute os comandos no terminal em modo de leitura (dry-run/audit), capture o `stdout` e `stderr`, e utilize esses logs para alimentar o seu relatório de auditoria. Caso a execução falhe por ambiente quebrado, ferramenta indisponível ou outro impedimento externo, registre o erro no relatório e siga o método de Fallback Agnóstico para analisar os manifestos e imports manualmente.

Siga a árvore de decisão abaixo de acordo com a stack detectada na Fase 1:

**1. Para Ecossistemas Node.js / npm / yarn:**

- **Vulnerabilidades:** Execute `npm audit --json` (ou `yarn audit`). Analise o JSON resultante para encontrar CVEs.
- **Deprecated:** Execute um linter ou processo de build sem emissão de arquivos (ex: `tsc --noEmit` se for TypeScript) e capture os warnings de funções ou pacotes marcados como `@deprecated`.

**2. Para Ecossistemas Python:**

- **Vulnerabilidades:** Faça a leitura do arquivo de manifesto (`requirements.txt`, `Pipfile` ou `pyproject.toml`). Como não devemos instalar pacotes no ambiente do usuário (evite `pip install`), cruze as versões declaradas nestes arquivos com sua base de conhecimento atualizada ou valide através da API pública do OSV (Open Source Vulnerabilities).
- **Deprecated:** Execute o linter configurado no projeto (ex: `flake8`, `pylint`) ou invoque o interpretador com flags de aviso (`python -Wd -m py_compile <arquivo_principal>.py`) para capturar `DeprecationWarning` no log.

**3. Para Ecossistemas .NET / C#:**

- **Vulnerabilidades:** Execute o comando nativo `dotnet list package --vulnerable` e analise a saída do terminal.
- **Deprecated:** Execute `dotnet build` e filtre a saída do terminal buscando pelos códigos de aviso padrão do compilador relacionados a anotações `[Obsolete]` (ex: warnings CS0612, CS0618).

**4. Para Ecossistemas Java (Maven / Gradle):**

- **Vulnerabilidades:** Se for Maven, execute `mvn org.owasp:dependency-check-maven:check`. Se não houver plugin configurado, leia o `pom.xml` ou `build.gradle` e cruze as versões com vulnerabilidades conhecidas (CVEs).
- **Deprecated:** Execute `mvn clean compile` ou `gradle build -x test`. Analise o log de build procurando por warnings de "uses or overrides a deprecated API".

**5. Outras Linguagens (Fallback Agnóstico):**

- Caso o projeto utilize uma stack não listada acima, faça o "parse" manual dos arquivos de configuração de dependências (manifestos) e das declarações de importação no topo dos arquivos fonte. Cruze essas informações com o seu conhecimento sobre bibliotecas descontinuadas ou sabidamente inseguras para aquela comunidade.

**Regra de Ouro:** Não modifique, instale ferramentas globais ou altere o estado da máquina hospedeira durante esta etapa de coleta. Apenas leia manifestos, invoque auditorias nativas ou capture logs de compilação.

### Coleta de findings estáticos (anti-patterns)

Varra todos os arquivos do projeto, incluindo as subpastas e procure por problemas. Utilize o [catalogo de anti-patterns](references/catalogo_antipatterns/INDEX.md) como referência. O catálogo tem exemplos em várias linguagens: `Python`, `Node/Typescript`, `Java`, `C#` e cada exemplo do catálogo foi escrito em uma dessas linguagens. Isto não significa que o tipo de finding se aplica somente à linguagem em que o exemplo foi escrito. Os findings do catálogo se aplicam à todas as linguagens e frameworks.

Principais tipos de findings que devem ser procurados:

**Segurança:**

- dados sensiveis hardcoded
- exposição de dados sensiveis em APIs
- log de dados sensíveis.
- dados de senha não criptografados
- dados criptografados com algoritmos fáceis de quebrar.
- sql injection

**Organização de código**:

- god class / god files: arquivos e/ou classes com muitas responsabilidades (não adoção do principio SOLID **Single Responsibily Principle - SRP**)
- classes de dominios diferentes no mesmo arquivo
- tipagem fraca (ausência de tipos ou uso do tipo `any`, `object` em linguagens que suportam tipagem estática)
- métodos muito longos: geram muita complexidade e devem ser quebrados em métodos menores ou outras classes (não adoção do principio SOLID **SRP**)
- obsessão por tipos primitivos e long parameter list: quando uma função tem muitos parâmetros, principalmente se forem tipos primitivos (string, number, boolean), isso é um sinal de que os dados estão mal estruturados e deveriam ser encapsulados em objetos ou classes de domínio.
- dependência de classes concretas (dependa de abstrações sempre que possivel e utilize um container de injeção de dependência para resolver as dependências)
- ausência dos demais principios SOLID, quando aplicável.
- falta de encapsulamento
- alto acoplamento, baixa coesão.
- nomes de variáveis, métodos, classes sem semântica (letras soltas, abreviaturas que nao indicam a intencao)
- repetição de código (ausência do principio **Don't Repeat Youserlf - DRY**)

**Padrões:**

- ausencia de padrão MVC
- falta de padrão repository para acesso à banco de dados
- aninhamento de blocos de código (if, for, while)
- SELECT N+1
  - implicito: quando estiver utilizando ORM
  - explicito: quando estiver utilizando query em loop

Você pode e deve reportar outros findings que forem encontrados e não estejam no catálogo.  

### Checklist de Validação

- [ ] Relatório segue o template definido nos arquivos de referência
- [ ] Cada finding tem arquivo e linhas exatos
- [ ] Findings ordenados por severidade (CRITICAL → LOW)
- [ ] Detecção de APIs deprecated incluída (se aplicável)
- [ ] Ferramenta nativa de auditoria (ex: npm audit) ou verificação estática de manifesto (OSV) executada com sucesso.
- [ ] Logs de build/linter capturados e analisados em busca de APIs obsoletas.

------

## Fase 3: Instruções de refatoração do projeto

Nesta fase vamos resolver os findings encontrados na fase 2 e refatorar o projeto para o padrão MVC, caso ainda não esteja nesta padrão.

### Instruções de fluxo

Ao finalizar a Fase 2, encerre a sua resposta atual com a pergunta: "Deseja prosseguir com a refatoração para o padrão MVC?". Aguarde a resposta do usuário antes de executar as instruções da Fase 3.

- Em caso negativo pare a execução.
- Em caso positivo, prossiga.

### Estrutura do projeto
- A estrutura do projeto deve seguir o [template](assets/template-projeto-mvc.md)
- Jamais altere a linguagem original do projeto. 
- Somente altere o framework principal do projeto se ele não for amigável ao padrão MVC. 
- Faça as refatorações necessárias. Você tem liberdade para incluir novas dependência que entender necessário para implementar as refatorações

### Persistência de Dados (Banco de Dados)
-**Uso preferencial de ORM:** Ao refatorar a camada de acesso a dados (Repositories/Models), você **DEVE**
introduzir e configurar um framework de ORM padrão ou um Query Builder robusto da stack do projeto (ex: SQLAlchemy para Python, Prisma/TypeORM para Node.js, Entity Framework para C#, Hibernate para Java).
- É estritamente proibido utilizar bibliotecas de *raw SQL* puro (ex: `sqlite3`, `pg`, `mysql2` puras)para operações de CRUD, a menos que seja estritamente necessário para uma query analítica muito complexa ou o framework não ofereça alternativa.
- Configure a conexão do ORM isolada no arquivo/módulo de configuração e injete nos repositórios.

### Documentação de APIs (Padrão OpenAPI 3.0)

Sempre que o projeto possuir endpoints de API (Controllers ou Rotas), você deve garantir que eles sejam documentados utilizando a especificação OpenAPI 3.0. 

Para manter o comportamento agnóstico e respeitar a cultura de cada framework, aplique a seguinte estratégia de decisão:

**1. Abordagem "Code-First" (Para frameworks com suporte nativo/tipado):**
Se o framework detectado possuir ecossistemas maduros para geração automática de OpenAPI via código, injete as anotações, decorators ou tipagens corretas nos Controllers e DTOs/Models.
* *Exemplos:* FastAPI no Python, Spring Boot (SpringDoc) no Java, NestJS no Node, ASP.NET Core no C#.
* *Ação:* Refatore os métodos adicionando descrições, tipos de retorno (200, 400, 404) e tipagem de payload nas assinaturas.

**2. Abordagem "Contract-First" (Para frameworks minimalistas ou de script):**
Se o framework for minimalista e exigir anotações em comentários (JSDoc) excessivamente longas que poluem a leitura, não modifique os arquivos de rotas com comentários.
* *Exemplos:* Express.js no Node, Flask puro no Python.
* *Ação:* Crie um arquivo standalone chamado `openapi.yaml` na raiz do projeto e escreva a especificação completa da API mapeada (paths, methods, components/schemas e responses).

**Critérios Mínimos da Especificação OpenAPI (independente da abordagem):**
- Título, Versão e Descrição da API.
- Para cada rota: Resumo (summary), tags (agrupadas por domínio/Controller).
- Mapeamento claro dos parâmetros (path, query, header).
- Definição de Schemas de Request Body (referenciando as Models/DTOs refatoradas).
- Respostas possíveis com seus respectivos HTTP Status Codes e Schemas de retorno.

### Passo a passo da refatoração

A partir da classificação dos findings encontrados na fase 2 comece refatorando pelos findings na seguinte ordem: CRITICAL, HIGH, MEDIUM, LOW.  
Procure resolver os findings individualmente. Caso não seja possivel resolva em conjunto.
Para cada finding encontrado:

**1. Planeje como resolvê-la**:
Utilize o [catalogo de anti-patterns](references/catalogo_antipatterns/INDEX.md) como referência para resolver os findings encontrados. O catálogo tem exemplos em várias linguagens: Python, Node/Typescript, Java, C#. Isto não significa que o exemplo se aplica somente à linguagem do exemplo. Apresentamos exemplos em várias linguagens para termos mais variedades, já que somos agnósticos à tecnologia. Caso o exemplo do anti-pattern esteja em um projeto de uma linguagem/framework diferente do exemplo, adapte. Caso o finding encontrado não esteja no catálogo, utilize as boas práticas de engenharia de software e arquitetura para planejar a refatoração. 

**2. Verifique se há testes relacionados com a mudança que será realizada**

**3. Execute a implementação**
**4. Execute os testes relacionados**:
Execute os testes relacionados com a mudança. Se houver falhas, siga este procedimento iterativo usando a ferramenta de terminal:

- Execute os testes e capture os logs de saída.
- Se falharem, analise o erro apresentado e aplique uma correção no código.
- Execute novamente os testes relacionados.
- Limite-se a no máximo 3 tentativas totais na conversa atual.

Se após 3 tentativas os testes continuarem falhando, reverta a alteração e notifique o usuário, anexando os logs e uma breve descrição das tentativas feitas.

### Rodando a aplicação refatorada

- Certifique-se que seja possivel rodar a aplicação a partir do `path` sem nenhuma dependência de arquivos externos ao `path`.
- Arquivos de configurações de dependências como `requirements.txt`, `package.json`, `build.gradle` devem estar no `path`.
- Gere um arquivo `README.md` com instruções de como baixar dependências e rodar o projeto.

### Checklist de Validação

- [ ] Estrutura de diretórios segue padrão MVC
- [ ] Configuração extraída para módulo de config (sem hardcoded)
- [ ] Models criados para abstrair dados
- [ ] Views/Routes separadas para visualização ou roteamento
- [ ] Controllers concentram o fluxo da aplicação
- [ ] Error handling centralizado
- [ ] Entry point claro
- [ ] Aplicação inicia sem erros
- [ ] Endpoints originais respondem corretamente
- [ ] Arquivo de dependências configurado com sucesso
- [ ] Arquivo `README.md` gerado com sucesso.
