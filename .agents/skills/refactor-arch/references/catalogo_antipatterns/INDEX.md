# Catálogo de Anti-patterns de Arquitetura e Código para Refatoração

Este catálogo serve como um guia de referência completo para identificação, análise e refatoração de problemas comuns de segurança, organização de código e padrões de arquitetura em sistemas baseados no ecossistema MVC.

## Estrutura do Catálogo

### 1. Segurança
* [Dados Sensíveis Hardcoded](seguranca/dados_sensiveis_hardcoded.md) (**Java**)
* [Exposição de Dados Sensíveis em APIs](seguranca/exposicao_dados_apis.md) (**Node/TypeScript**)
* [Log de Dados Sensíveis](seguranca/log_dados_sensiveis.md) (**Python**)
* [Dados de Senha Não Criptografados](seguranca/senhas_nao_criptografadas.md) (**C#**)
* [Criptografia com Algoritmos Fracos](seguranca/criptografia_fraca.md) (**Java**)
* [SQL Injection](seguranca/sql_injection.md) (**Python**)
* [Deprecated Depencies](seguranca/dependencies_deprecated.md) (**Node/Typescript**)

### 2. Organização de Código
* [god class / files](organizacao/god_class.md) (**C#**)
* [Métodos Muito Longos](organizacao/metodos_longos.md) (**Node/TypeScript**)
* [Falta de Encapsulamento](organizacao/falta_encapsulamento.md) (**Java**)
* [Dominio Anêmico](organizacao/dominio_anemico.md) (**Node/TypeScript**)
* [Alto Acoplamento e Baixa Coesão](organizacao/acoplamento_coesao.md) (**Python**)
* [Dependência de Classes Concretas](organizacao/dependencia_concreta.md) (**C#**)
* [Nomes de Variáveis Sem Semântica](organizacao/nomes_sem_semantica.md) (**Node/TypeScript**)
* [Repetição de Código (DRY Violation)](organizacao/repeticao_codigo.md) (**Java**)
* [Números e Strings mágicas](organizacao/numeros_strings_magicas.md) (**Java**)
* [Obsessão por tipos primitivos](organizacao/obsessao_primitivos_parametro.md) (**Java**)
* [Tipagem fraca](organizacao/multiplas_classes_tipagem_fraca.md) (**Java**)

### 3. Padrões de Projeto e Arquitetura
* [Ausência do Padrão MVC](padroes/ausencia_mvc.md) (**Python**)
* [Falta de Padrão Repository](padroes/falta_repository.md) (**C#**)
* [Aninhamento Excessivo de Blocos (Arrow Anti-pattern)](padroes/aninhamento_blocos.md) (**Node/TypeScript**)
* [Problema do SELECT N+1 (Implícito e Explícito)](padroes/select_n_plus_1.md) (**Java e Python**)
