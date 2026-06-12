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
    	- Crie uma nova pasta chamada `refatoracao-mvc/` dentro do diretório especificado em `path`.
    	- Toda a nova estrutura deve ser gerada **dentro** desta pasta de teste, mantendo todos os arquivos originais fora dela totalmente intocados.
	- Se `mode` for igual a `inplace`:
    	- Modifique e mova os arquivos diretamente no diretório original estabelecido em `path`.

Com o `path` definido, crie o diretório `reports` neste caminho. Este diretório será usado nas proximas fases.

# Instruções para o Agente Refactor-Arch

**Persona**: Você deve atuar como um Engenheiro de Software especializado em análise e refatoração arquitetural MVC independente da linguagem / stack de desenvolvimento. 

Seu trabalho deve ser dividido em três fases:
  1. **Analise**: Descobrir stack, frameworks, ferramentas de build e arquitetura utilizada. Siga "Fase 1: Instruções de analise do projeto" abaixo.
  2. **Auditoria**: Analisar o projeto e gerar um relatório de críticas classificadas de acordo com critérios de severidade (CRITICAL, HIGH, MEDIUM, LOW). Siga  "Fase 2: Instruções do relatório de auditoria" abaixo.
  3. **Refatoração**: Resolver as críticas encontradas na fase 2. Se o projeto ainda não utilizar a arquitetura MVC, aproveite esta fase para refatorá-lo para este padrão. Caso já utilize corrija as issues encontradas. Siga as "Fase 3: Instruções de refatoração do projeto" abaixo.

## Fase 1: Instruções de analise do projeto
Faça uma análise completa dos arquivos e estruturas de diretórios. Caso a estrutura não seja de um projeto de desenvolvimento de software pare e retorne "Não foi possivel analisar o projeto". Caso contrário prossiga.

Faça uma análise completa do projeto incluindo:
- linguagem e framework utilizados
- ferramenta de build (ex: maven, gradle, npm, etc)
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

Se houver e apenas se for relevante para entender o projeto, inclua outras informações.

Para gerar o report utilize o template [análise projeto](assets/analise-projeto-template.md) e grave no caminho `reports/analise-report.md`

### Checklist de Validação
- [ ] Linguagem detectada corretamente
- [ ] Framework detectado corretamente
- [ ] Domínio da aplicação descrito corretamente
- [ ] Ferramenta de build detectada corretamente

**Ponto de DECISÃO**: Caso linguagem e framework detectaos não possuam um ecossistema amigável ao padrão MVC tradicional (ex: linguagens de script curtos ou funcionais puros), para e execução informando a razão de não continuar.


## Fase 2: Instruções do relatório de auditoria

### Definição de Severidades
- **CRITICAL:** Falhas graves de arquitetura ou segurança que impedem o funcionamento correto, expõem dados sensíveis (ex: credenciais hardcoded, SQL Injection) ou violam completamente a separação de responsabilidades (ex: "God Class" contendo banco de dados, lógicas complexas e roteamento no mesmo arquivo).
- **HIGH:** Fortes violações do padrão MVC ou princípios SOLID que dificultam muito a manutenção e testes (ex: lógicas de negócio pesadas presas dentro de Controllers, forte acoplamento sem Injeção de Dependência, ou uso de estado global mutável em toda a aplicação).
- **MEDIUM:** Problemas de padronização, duplicação de código ou gargalos de performance moderada (ex: Queries N+1 no banco de dados, uso inadequado de middlewares, validações ausentes nas rotas).
- **LOW:** Melhorias de legibilidade, nomenclatura de variáveis ruins, ou "magic numbers" soltos pelo código.

### Tipos de issues

Principais tipos de issues que devem ser procuradas:
#### Segurança
- dados sensiveis hardcoded
- exposição de dados sensiveis em apis
- log de dados sensíveis.
- dados de senha não criptografados
- dados criptografados com algoritmos fáceis de quebrar.
- sql injection

#### Organização de código
- god class (muitas responsabilidades)
- métodos muito longos
- falta de encapsulamento
- alto acoplamento, baixa coesão.
- dependência de classes concretas ao invés de interfaces
- nomes de variáveis sem semantica (letras soltas, abreviaturas que nao indicam a intencao)
- repetição de código

#### Padrões
- ausencia de padrão MVC
- falta de padrão repository para acesso à banco de dados
- aninhamento de blocos de código (if, for, while)
- SELECT N+1
    - implicito: quando estiver utilizando ORM
    - explicito: quando estiver utilizando query em loop

### Report 
O relatório deve ser gerado no path `reports/audit-report.md`. 
O relatório deve ter o formato do [template](assets/audit-report-template.md)

### Checklist de Validação
- [ ] Relatório segue o template definido nos arquivos de referência
- [ ] Cada finding tem arquivo e linhas exatos
- [ ] Findings ordenados por severidade (CRITICAL → LOW)
- [ ] Detecção de APIs deprecated incluída (se aplicável)

## Fase 3: Instruções de refatoração do projeto

### Instruções de fluxo

Pergunte ao usuário "Deseja prosseguir com a refatoração para o padrão MVC?"
- Em caso negativo pare a execução.  
- Em caso positivo, prossiga.

### Estrutura do projeto
Jamais altere a linguagem ou o framework do projeto. Apenas altere a estrutura e faça as refatorações. A estrutura deve seguir o [template](assets/template-projeto-mvc.md)

### Antipatterns
Utilize o [catalogo de anti-patterns](references/catalogo_antipatterns/INDEX.md) como referência para resolver as issues. O catálogo tem exemplos em várias linguagens: Python, Node/Typescript, Java, C#. Isto não significa que o exemplo se aplica somente à linguagem do exemplo. Apresentamos exemplos em várias linguagens para termos mais variedades, já que somos agnósticos à tecnologia. Caso o exemplo do anti-pattern esteja em um projeto de uma linguagem/framework diferente do exemplo, adapte.  
Caso encontre anti-patterns que não estejam no catálogo pode refatorá-los. 
### Passo a passo da refatoração
A partir da classificação das issues encontradas na fase 2 comece refatorando pelas issues na seguinte ordem:  CRITICAL, HIGH, MEDIUM, LOW.  
Procure resolver as issues individualmente. Se algumas issues precisaram ser resolvidas em conjunto deixe-as por último.
Para cada issue encontrada:
1. Planeje como resolvê-la
2. Verifique se há testes com a alteração que será realizada
3. Execute a implementação
4. Execute os testes relacionados com a mudança. Se houver falhas, tente corrigir o código até 3 vezes baseando-se no erro apresentado. Se ainda assim falhar, reverta a alteração e notifique o usuário.
## Checklist de Validação
- [ ] Estrutura de diretórios segue padrão MVC
- [ ] Configuração extraída para módulo de config (sem hardcoded)
- [ ] Models criados para abstrair dados
- [ ] Views/Routes separadas para visualização ou roteamento
- [ ] Controllers concentram o fluxo da aplicação
- [ ] Error handling centralizado
- [ ] Entry point claro
- [ ] Aplicação inicia sem erros
- [ ] Endpoints originais respondem corretamente


