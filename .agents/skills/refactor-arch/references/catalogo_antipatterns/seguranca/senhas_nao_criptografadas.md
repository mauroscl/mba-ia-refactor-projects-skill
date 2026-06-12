# Anti-pattern: Dados de Senha Não Criptografados
**Linguagem de Exemplo:** C#

## Descrição
Tratar ou armazenar senhas de usuários em texto limpo (Plain Text) no banco de dados ou arquivos locais. Se o banco for comprometido por vazamento ou SQL Injection, todas as contas dos clientes ficam vulneráveis imediatamente.

## Como NÃO Fazer
```csharp
using System.Data.SqlClient;

public class UserService
{
    private string connectionString = "Server=db_server;Database=app;User Id=sa;Password=secret;";

    public void RegisterUser(string username, string plainPassword)
    {
        using (SqlConnection conn = new SqlConnection(connectionString))
        {
            // PROBLEMA: A senha é inserida no banco em texto claro sem qualquer hash criptográfico
            string query = "INSERT INTO Users (Username, Password) VALUES (@username, @password)";
            SqlCommand cmd = new SqlCommand(query, conn);
            cmd.Parameters.AddWithValue("@username", username);
            cmd.Parameters.AddWithValue("@password", plainPassword); 
            
            conn.Open();
            cmd.ExecuteNonQuery();
        }
    }
}
```

## Como Fazer Corretamente
```csharp
using System.Data.SqlClient;
using BCrypt.Net; // Utilizando pacote seguro BCrypt.Net-Next

public class UserService
{
    private string connectionString = "Server=db_server;Database=app;User Id=sa;Password=secret;";

    public void RegisterUser(string username, string plainPassword)
    {
        // SOLUÇÃO: Gerar hash unidirecional seguro com salt embutido automaticamente
        string passwordHash = BCrypt.Net.BCrypt.HashPassword(plainPassword, workFactor: 12);

        using (SqlConnection conn = new SqlConnection(connectionString))
        {
            string query = "INSERT INTO Users (Username, PasswordHash) VALUES (@username, @passwordHash)";
            SqlCommand cmd = new SqlCommand(query, conn);
            cmd.Parameters.AddWithValue("@username", username);
            cmd.Parameters.AddWithValue("@passwordHash", passwordHash);
            
            conn.Open();
            cmd.ExecuteNonQuery();
        }
    }
}
```

## Impacto da Refatoração
- Segurança Base: Mesmo com acesso total às tabelas do banco, invasores não conseguem reverter o hash para descobrir a senha original do usuário.

- Resistência: O fator de trabalho do BCrypt atrasa exponencialmente tentativas de ataques de força bruta ou Rainbow Tables.