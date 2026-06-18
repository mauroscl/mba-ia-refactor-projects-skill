# Anti-pattern: Falta de Encapsulamento
**Linguagem de Exemplo:** Java

## Descrição
Expor campos internos de um modelo de domínio de maneira pública ou fornecer métodos modificadores (setters) irrestritos que quebram as invariantes de negócio, permitindo que estados inconsistentes sejam forçados de qualquer ponto da aplicação.

## Como NÃO Fazer
```java
package com.empresa.mvc.model;

public class ContaBancaria {
    // PROBLEMA: Atributos públicos permitem mutação direta e perigosa por qualquer classe externa
    public String numeroConta;
    public double saldo;

    public ContaBancaria(String numeroConta, double saldo) {
        this.numeroConta = numeroConta;
        this.saldo = saldo;
    }
}

// Exemplo do perigo:
// ContaBancaria conta = new ContaBancaria("123", 500);
// conta.saldo = -99999.00; // Estado corrompido sem validação de regras de saque
```

## Como Fazer Corretamente
```java
package com.empresa.mvc.model;

public class ContaBancaria {
    // SOLUÇÃO: Atributos estritamente privados com controle interno de comportamento
    private final String numeroConta;
    private double saldo;

    public ContaBancaria(String numeroConta, double saldoInicial) {
        if (saldoInicial < 0) {
            throw new IllegalArgumentException("Saldo inicial não pode ser negativo.");
        }
        this.numeroConta = numeroConta;
        this.saldo = saldoInicial;
    }

    public String getNumeroConta() {
        return numeroConta;
    }

    public double getSaldo() {
        return saldo;
    }

    // A mutação do estado passa obrigatoriamente por um método de negócio que valida a operação
    public void depositar(double valor) {
        if (valor <= 0) {
            throw new IllegalArgumentException("O valor do depósito deve ser positivo.");
        }
        this.saldo += valor;
    }

    public void sacar(double valor) {
        if (valor <= 0) {
            throw new IllegalArgumentException("O valor do saque deve ser positivo.");
        }
        if (this.saldo - valor < 0) {
            throw new IllegalStateException("Saldo insuficiente para concluir o saque.");
        }
        this.saldo -= valor;
    }
}
```

## Impacto da Refatoração
- Consistência de Dados: Garante que o objeto nunca entre em estado inválido na memória da aplicação.

- Abstração: Modificações na forma como o saldo é calculado internamente não afetam quem chama os métodos públicos.