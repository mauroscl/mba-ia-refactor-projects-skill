# Anti-pattern: God Class
**Linguagem de Exemplo:** C#

## Descrição
Descrição
Uma única classe assume múltiplos papéis e responsabilidades distintas dentro do sistema (violação do Single Responsibility Principle - SRP). Elas se tornam gigantescas, com alto acoplamento interno e difíceis de testar isoladamente.

## Como NÃO Fazer
```csharp
public class EmployeeManager
{
    // PROBLEMA: Esta classe gerencia persistência, validação, cálculo de folha e geração de arquivos.
    public void SaveEmployeeToDatabase(Employee emp) { /* ... */ }
    public void ValidateEmployeeData(Employee emp) { /* ... */ }
    public decimal CalculateNetSalary(Employee emp) { /* ... */ }
    public void GenerateEmployeePdfReport(Employee emp) { /* ... */ }
    public void SendNotificationEmail(string email, string message) { /* ... */ }
}```

## Como Fazer Corretamente
```csharp
// SOLUÇÃO: Divisão em classes coesas focadas em uma única responsabilidade central.

public class EmployeeRepository
{
    public void Save(Employee emp) { /* Lógica de Banco de Dados */ }
}

public class EmployeeValidator
{
    public bool Validate(Employee emp) { /* Lógica de Validação Semântica */ }
}

public class PayrollCalculator
{
    public decimal CalculateNetSalary(Employee emp) { /* Regras de Negócio de Salário */ }
}

public class EmployeeReportGenerator
{
    public byte[] GeneratePdf(Employee emp) { /* Formatação de Relatório */ }
}

public class EmailNotificationService
{
    public void Send(string targetEmail, string body) { /* Comunicação SMTP */ }
}
```

## Impacto da Refatoração
- Manutenibilidade: Modificações nas regras de pagamento não quebram acidentalmente o envio de e-mails ou rotinas de banco.

- Testabilidade: Cada componente pode ser coberto por testes unitários limpos com mocks simples.