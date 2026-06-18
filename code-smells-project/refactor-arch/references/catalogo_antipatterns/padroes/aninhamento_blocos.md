# Anti-pattern: Aninhamento Excessivo
**Linguagem de Exemplo:** Node.js

## Como NÃO Fazer
```typescript
function processDiscountValidation(user: any, cart: any): boolean {
    // PROBLEMA: Aninhamento profundo de condicionais dificulta o rastreio mental do caminho feliz
    if (user !== null) {
        if (user.isPremium) {
            if (cart !== null) {
                if (cart.items.length > 0) {
                    if (cart.totalValue > 200) {
                        return true;
                    } else {
                        return false;
                    }
                } else {
                    return false;
                }
            } else {
                return false;
            }
        } else {
            return false;
        }
    } else {
        return false;
    }
}
```

## Como Fazer Corretamente
```typescript
// SOLUÇÃO: Uso estratégico de Guard Clauses (Cláusulas de Guarda) para inversão rápida de fluxo

function processDiscountValidationClean(user: any, cart: any): boolean {
    // Validações de guarda eliminam ramificações aninhadas e limpam a leitura do método
    if (!user || !user.isPremium) return false;
    if (!cart || cart.items.length === 0) return false;
    
    // O objetivo central (Caminho Feliz) é posicionado de forma linear na base da função
    const isValueEligibleForDiscount = cart.totalValue > 200;
    return isValueEligibleForDiscount;
}
```

## Impacto da Refatoração
- Complexidade Ciclomática: Reduz drasticamente as ramificações lógicas do código.

- Legibilidade Imediata: Desenvolvedores conseguem identificar instantaneamente os critérios de rejeição logo nas primeiras linhas.