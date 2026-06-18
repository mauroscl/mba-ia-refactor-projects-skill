# Anti-pattern: Dados Sensíveis Hardcoded
**Linguagem de Exemplo:** Java

## Descrição
Inserir credenciais de acesso, chaves de API, senhas ou tokens de autenticação diretamente no código-fonte.

## Como NÃO Fazer
```java
package com.empresa.mvc.config;

import java.sql.Connection;
import java.sql.DriverManager;

public class DatabaseConnection {
    // PROBLEMA: Credenciais confidenciais expostas
    private static final String URL = "jdbc:postgresql://production-db.internal/db";
    private static final String USER = "admin";
    private static final String PASSWORD = "SecretPassword123!";

    public static Connection getConnection() throws Exception {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }
}
```

## Como Fazer Corretamente
```java
package com.empresa.mvc.config;

import java.sql.Connection;
import java.sql.DriverManager;

public class DatabaseConnection {
    // SOLUÇÃO: Leitura das credenciais através de variáveis de ambiente
    private static final String URL = System.getenv("DB_URL");
    private static final String USER = System.getenv("DB_USER");
    private static final String PASSWORD = System.getenv("DB_PASSWORD");

    public static Connection getConnection() throws Exception {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }
}
```