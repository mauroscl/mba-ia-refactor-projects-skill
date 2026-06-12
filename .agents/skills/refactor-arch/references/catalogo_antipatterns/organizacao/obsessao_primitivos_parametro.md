# Anti-pattern: Obsessão por Tipos Primitivos e Parâmetros Excessivos
**Linguagem de Exemplo:** Node.js / TypeScript

## Descrição
Ocorre quando o sistema utiliza tipos básicos da linguagem (strings, números, booleanos) para representar conceitos de domínio que deveriam ser objetos, resultando em funções procedurais com listas gigantescas de parâmetros. Isso destrói o encapsulamento, facilita a troca acidental da ordem dos argumentos e impede a validação isolada dos dados.

## Como NÃO Fazer
```typescript
// PROBLEMA 1: Código puramente procedural.
// PROBLEMA 2: Assinatura de método gigante (Long Parameter List).
// PROBLEMA 3: Obsessão por primitivos (CPF, CEP, Moeda são tratados apenas como strings/numbers soltos).

export function processEmployeeOnboarding(
    firstName: string, 
    lastName: string, 
    cpf: string, 
    rg: string, 
    street: string, 
    city: string, 
    zipCode: string, 
    baseSalary: number, 
    bonus: number
): void {
    if (cpf.length !== 11) throw new Error("CPF inválido");
    if (baseSalary < 0) throw new Error("Salário não pode ser negativo");

    console.log(`Registrando funcionário: ${firstName} ${lastName}`);
    console.log(`Enviando kit para: ${street}, ${city} - ${zipCode}`);
    console.log(`Remuneração Total: ${baseSalary + bonus}`);
}

## Como fazer corretamente
// SOLUÇÃO: Agrupar primitivos em Classes ou Objetos de Valor (Value Objects) 
// com suas próprias validações de estado e regras de negócio.

export class Document {
    constructor(public readonly cpf: string, public readonly rg: string) {
        if (cpf.length !== 11) throw new Error("CPF inválido");
    }
}

export class Address {
    constructor(public readonly street: string, public readonly city: string, public readonly zipCode: string) {}
}

export class Remuneration {
    constructor(public readonly baseSalary: number, public readonly bonus: number) {
        if (baseSalary < 0) throw new Error("Salário não pode ser negativo");
    }
    
    get total(): number {
        return this.baseSalary + this.bonus;
    }
}

// O funcionário agora é uma entidade coesa e o onboarding recebe um único parâmetro tipado.
export class Employee {
    constructor(
        public readonly firstName: string,
        public readonly lastName: string,
        public readonly document: Document,
        public readonly address: Address,
        public readonly remuneration: Remuneration
    ) {}

    public processOnboarding(): void {
        console.log(`Registrando funcionário: ${this.firstName} ${this.lastName}`);
        console.log(`Enviando kit para: ${this.address.street}, ${this.address.city} - ${this.address.zipCode}`);
        console.log(`Remuneração Total: ${this.remuneration.total}`);
    }
}
```

## Impacto da Refatoração
- Desacoplamento e Testabilidade: Agora é possível testar as regras de validação de Document ou o cálculo de Remuneration de forma totalmente isolada do fluxo de admissão.

- Prevenção de Erros: É impossível passar um CEP no lugar de um CPF acidentalmente, pois a tipagem forte das classes impede essa troca de parâmetros na compilação.
