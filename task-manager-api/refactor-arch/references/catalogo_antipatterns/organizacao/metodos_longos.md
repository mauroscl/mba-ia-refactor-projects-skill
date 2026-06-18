# Anti-pattern: Métodos Muito Longos
**Linguagem de Exemplo:** Node.js / TypeScript

## Descrição
Funções extensas contendo dezenas ou centenas de linhas que tentam executar o fluxo lógico completo em um único bloco. Dificultam a leitura de alto nível, mascaram duplicações e inviabilizam o reuso de sub-rotinas.

## Como NÃO fazer
```typescript
async function processOrderCheckout(orderId: string, userId: string, paymentToken: string): Promise<void> {
    // PROBLEMA: Um único bloco orquestra validação, estoque, pagamento, gravação e comunicação
    console.log("Iniciando fluxo...");
    const user = await db.findUser(userId);
    if (!user || !user.isActive) throw new Error("Usuário inválido");
    
    const order = await db.findOrder(orderId);
    if (order.status !== "PENDING") throw new Error("Pedido não está pendente");
    
    let total = 0;
    for (const item of order.items) {
        const stock = await db.checkStock(item.id);
        if (stock < item.qty) throw new Error(`Sem estoque para o item: ${item.name}`);
        total += item.price * item.qty;
    }
    
    const paymentResult = await gateway.charge(paymentToken, total);
    if (!paymentResult.success) {
        throw new Error("Pagamento rejeitado");
    }
    
    order.status = "PAID";
    await db.updateOrder(order);
    
    await emailService.send(user.email, "Seu pagamento foi aprovado!");
}
```

## Como Fazer Corretamente
```typescript
// SOLUÇÃO: Decomposição em pequenos métodos explicativos e auto-documentados
async function processOrderCheckoutRefactored(orderId: string, userId: string, paymentToken: string): Promise<void> {
    const user = await validateUserStatus(userId);
    const order = await validateOrderPending(orderId);
    
    await verifyStockAvailability(order.items);
    
    await executeOrderPayment(paymentToken, order.calculateTotal());
    
    await finalizeOrderState(order);
    await sendConfirmationEmail(user.email);
}

async function validateUserStatus(userId: string) {
    const user = await db.findUser(userId);
    if (!user || !user.isActive) throw new Error("Usuário inválido");
    return user;
}

async function validateOrderPending(orderId: string) {
    const order = await db.findOrder(orderId);
    if (order.status !== "PENDING") throw new Error("Pedido não está pendente");
    return order;
}

async function verifyStockAvailability(items: any[]) {
    for (const item of items) {
        const stock = await db.checkStock(item.id);
        if (stock < item.qty) throw new Error(`Sem estoque para o item: ${item.name}`);
    }
}

async function executeOrderPayment(token: string, amount: number) {
    const paymentResult = await gateway.charge(token, amount);
    if (!paymentResult.success) throw new Error("Pagamento rejeitado");
}

async function finalizeOrderState(order: any) {
    order.status = "PAID";
    await db.updateOrder(order);
}

async function sendConfirmationEmail(email: string) {
    await emailService.send(email, "Seu pagamento foi aprovado!");
}
```

## Impacto da Refatoração
- Leitura Fluida: O método principal lê-se como prosa literária descrevendo a regra de negócio.

- Reuso: Métodos de validação isolados agora podem ser acionados por outros controllers do ecossistema.