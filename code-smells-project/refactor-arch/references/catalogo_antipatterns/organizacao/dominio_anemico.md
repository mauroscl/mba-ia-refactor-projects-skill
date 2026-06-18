# Anti-pattern: Domínio Anêmico (Anemic Domain Model)
**Linguagem de Exemplo:** Node.js / TypeScript

## Descrição
O Domínio Anêmico ocorre quando as entidades centrais do sistema são reduzidas a meras estruturas de dados (apenas um conjunto de propriedades públicas), enquanto toda a inteligência, validação e comportamento do negócio são movidos para classes externas de "Serviço" ou "Controllers". Isso gera código procedural disfarçado, dificultando a manutenção e espalhando regras de negócio por toda a aplicação.

## Como NÃO Fazer
```typescript
// --- arquivo: src/models/Order.ts ---
// PROBLEMA 1: A entidade é apenas um saco de dados burro (Anemic Model).
export class Order {
    public id: string;
    public status: string = "OPEN";
    public totalAmount: number = 0;
    public items: any[] = [];
}

// --- arquivo: src/services/OrderService.ts ---
import { Order } from "../models/Order";

export class OrderService {
    // PROBLEMA 2: O Serviço sequestra o comportamento que deveria pertencer ao Pedido.
    public addItem(order: Order, item: any): void {
        if (order.status !== "OPEN") {
            throw new Error("Não é possível adicionar itens a um pedido fechado.");
        }
        order.items.push(item);
        order.totalAmount += item.price;
    }

    public closeOrder(order: Order): void {
        if (order.items.length === 0) {
            throw new Error("Pedido vazio não pode ser fechado.");
        }
        order.status = "CLOSED";
    }
}
```

## Como fazer corretamente

```typescript
// --- arquivo: src/models/Order.ts ---
// SOLUÇÃO 1: Rich Domain Model (Modelo de Domínio Rico). A entidade dita e protege suas regras.
export class Order {
    private _status: string = "OPEN";
    private _totalAmount: number = 0;
    private _items: any[] = [];

    constructor(public readonly id: string) {}

    // Acesso apenas de leitura ao estado
    get status(): string { return this._status; }
    get totalAmount(): number { return this._totalAmount; }
    
    // Retorna uma cópia para evitar que o array seja modificado externamente (Encapsulamento)
    get items(): any[] { return [...this._items]; } 

    // SOLUÇÃO 2: A lógica de negócio reside junto aos dados que ela manipula.
    public addItem(item: any): void {
        if (this._status !== "OPEN") {
            throw new Error("Não é possível adicionar itens a um pedido fechado.");
        }
        this._items.push(item);
        this._totalAmount += item.price;
    }

    public close(): void {
        if (this._items.length === 0) {
            throw new Error("Pedido vazio não pode ser fechado.");
        }
        this._status = "CLOSED";
    }
}

// --- arquivo: src/services/OrderService.ts ---
import { Order } from "../models/Order";

export class OrderServiceRefactored {
    constructor(private orderRepository: any) {}

    // O Serviço volta ao seu papel correto: Orquestrar infraestrutura (banco de dados, transações),
    // mas delega as decisões puras de negócio para a própria Entidade.
    public async processNewItem(orderId: string, newItem: any): Promise<void> {
        const order: Order = await this.orderRepository.findById(orderId);
        
        // A entidade processa a regra e se protege sozinha. O serviço não precisa saber as regras de soma ou status.
        order.addItem(newItem); 
        
        await this.orderRepository.save(order);
    }
}
```

## Impacto da Refatoração
- Coesão Extrema: As regras sobre o ciclo de vida do pedido (como e quando adicionar um item) não estão espalhadas em dezenas de Services ou Controllers. Elas vivem unicamente na classe Order.

- Invariantes Garantidas: A remoção das propriedades públicas e a clonagem do array no get items() garantem que nenhuma outra parte do código consiga forçar acidentalmente um "status" incorreto ou injetar um item sem passar pelas validações oficiais.

- Simplificação de Testes Unitários: Para testar a lógica de cálculo do pedido, não é necessário simular bancos de dados ou mocks complexos no OrderService. Basta instanciar um new Order("123") na memória e testar seus métodos isoladamente.