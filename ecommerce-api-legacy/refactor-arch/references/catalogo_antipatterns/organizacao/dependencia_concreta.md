# Anti-pattern: Dependência Concreta
**Linguagem de Exemplo:** C#

## Descrição
Instanciar componentes diretamente dentro de classes de serviço ou controle usando a palavra-chave new. Isso amarra o código a implementações específicas de infraestrutura, impossibilitando a substituição por mocks durante testes de unidade e violando o Dependency Inversion Principle (DIP).  
O uso de classes com métodos estáticos também não é um boa prática. A exceção são métodos puros que não tenham nenhuma dependência externa. Sempre que estiver disponivel na linguagem/framework utilize um container de injeção de dependência. Caso ainda não exista um container, adicione´0 nas dependências e configure corretamente.

## Como NÃO Fazer
```csharp
public class OrderService
{
    // PROBLEMA: Dependência direta e engessada de uma classe concreta de infraestrutura externa
    private SqlDataPersistence _persistence = new SqlDataPersistence();
    private SmtpEmailSender _emailSender = new SmtpEmailSender();

    public void CompleteOrder(Order order)
    {
        _persistence.SaveOrderRecord(order);
        _emailSender.SendHtmlEmail(order.CustomerEmail, "Pedido Concluído");
    }
}```

## Como Fazer Corretamente
```csharp
// SOLUÇÃO: Definição de contratos abstratos (Interfaces)

public interface IOrderRepository
{
    void Save(Order order);
}

public interface INotificationService
{
    void SendNotification(string destination, string content);
}

public class OrderServiceRefactored
{
    private readonly IOrderRepository _orderRepository;
    private readonly INotificationService _notificationService;

    // Dependências injetadas via construtor guiadas pelo IoC container da aplicação
    public OrderServiceRefactored(IOrderRepository orderRepository, INotificationService notificationService)
    {
        _orderRepository = orderRepository;
        _notificationService = notificationService;
    }

    public void CompleteOrder(Order order)
    {
        _orderRepository.Save(order);
        _notificationService.SendNotification(order.CustomerEmail, "Pedido Concluído");
    }
}```

## Impacto da Refatoração
- Desacoplamento: A camada de aplicação desconhece se os dados são salvos em SQL Server, PostgreSQL ou memória.

- Testes Ágeis: Permite criar testes unitários instantâneos passando implementações falsas (Mocks/Stubs) das interfaces por parâmetro.