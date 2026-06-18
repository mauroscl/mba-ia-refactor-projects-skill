# Anti-pattern: Nomes sem Semântica
**Linguagem de Exemplo:** Node.js

## Descrição
Utilizar variáveis identificadas com letras únicas, abreviações misteriosas ou nomes genéricos que falham ao expressar a real intenção e o contexto de negócio daquele dado.

## Como NÃO Fazer
```typescript
function pData(arr: any[]): any[] {
    // PROBLEMA: O que significam 'arr', 'x', 'd', 'lst', 'fn'? Nenhuma clareza contextual.
    let lst: any[] = [];
    for (let i = 0; i < arr.length; i++) {
        let x = arr[i];
        let d = new Date().getTime() - new Date(x.dt).getTime();
        let fn = 30 * 24 * 60 * 60 * 1000;
        if (x.st === 1 && d > fn) {
            lst.push(x);
        }
    }
    return lst;
}
```

## Como Fazer Corretamente
```typescript
interface CustomerContract {
    activationDate: string;
    isActiveStatus: number;
    id: string;
}

// SOLUÇÃO: Nomes descritivos e semânticos que esclarecem o domínio do problema sem ambiguidades
function filterExpiredContracts(contracts: CustomerContract[]): CustomerContract[] {
    const expiredContracts: CustomerContract[] = [];
    const currentTimestamp = new Date().getTime();
    const thirtyDaysInMilliseconds = 30 * 24 * 60 * 60 * 1000;

    for (const contract of contracts) {
        const contractAgeInMilliseconds = currentTimestamp - new Date(contract.activationDate).getTime();
        const isContractActive = contract.isActiveStatus === 1;

        if (isContractActive && contractAgeInMilliseconds > thirtyDaysInMilliseconds) {
            expiredContracts.push(contract);
        }
    }
    return expiredContracts;
}
```

## Impacto da Refatoração
- Auto-documentação: Elimina a necessidade de comentários explicativos para traduzir o funcionamento do algoritmo.

- Segurança na Manutenção: Reduz drasticamente a inserção de bugs por desenvolvedores que venham a dar manutenção no código futuro.