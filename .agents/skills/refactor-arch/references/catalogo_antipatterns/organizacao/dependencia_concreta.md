# Anti-pattern: Dependência Concreta
**Linguagem de Exemplo:** C#

## Como NÃO Fazer
```csharp
public class OrderService {
    private SqlRepository repo = new SqlRepository(); // Acoplamento rígido
}
```

## Como Fazer Corretamente
```csharp
public class OrderService {
    private readonly IOrderRepository repo;
    public OrderService(IOrderRepository repository) {
        this.repo = repository; // Injeção de dependência
    }
}
```

## Impacto da Refatoração
- Desacoplamento: A camada de aplicação desconhece se os dados são salvos em SQL Server, PostgreSQL ou memória.

- Testes Ágeis: Permite criar testes unitários instantâneos passando implementações falsas (Mocks/Stubs) das interfaces por parâmetro.