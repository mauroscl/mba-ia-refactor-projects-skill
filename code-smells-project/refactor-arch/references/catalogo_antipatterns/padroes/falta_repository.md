# Anti-pattern: Falta de Repository
**Linguagem de Exemplo:** C#

## Como NÃO Fazer
```csharp
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

public class OrderController : Controller
{
    private readonly ApplicationDbContext _dbContext = new ApplicationDbContext();

    public async Task<IActionResult> GetActiveHighValueOrders()
    {
        var orders = await _dbContext.Orders
            .Where(o => o.IsActive && o.TotalAmount > 5000)
            .ToListAsync();

        return View(orders);
    }
}```

## Como Fazer Corretamente
```csharp
public interface IOrderRepository
{
    Task<IEnumerable<Order>> GetPremiumActiveOrdersAsync();
}

public class OrderRepository : IOrderRepository
{
    private readonly ApplicationDbContext _context;

    public OrderRepository(ApplicationDbContext context) { _context = context; }

    public async Task<IEnumerable<Order>> GetPremiumActiveOrdersAsync()
    {
        return await _context.Orders.Where(o => o.IsActive && o.TotalAmount > 5000).ToListAsync();
    }
}

public class OrderControllerRefactored : Controller
{
    private readonly IOrderRepository _orderRepository;
    public OrderControllerRefactored(IOrderRepository orderRepository) { _orderRepository = orderRepository; }

    public async Task<IActionResult> GetActiveHighValueOrders()
    {
        var orders = await _orderRepository.GetPremiumActiveOrdersAsync();
        return View(orders);
    }
}```