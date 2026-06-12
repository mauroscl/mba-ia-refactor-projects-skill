# Anti-pattern: Números e Strings Mágicas
**Linguagem de Exemplo:** Java

## Descrição
O uso de literais numéricos ou de texto espalhados diretamente pelo código fonte ("mágicos" porque seu significado não é imediatamente óbvio para quem lê). Isso dificulta a manutenção, pois uma simples alteração de regra de negócio exige uma busca global no projeto, aumentando o risco de inconsistências.

## Como NÃO Fazer

```java
package com.empresa.mvc.service;

public class PedidoService {
    public double calcularDesconto(double valorTotal, int perfilCliente) {
        // PROBLEMA: O que significa '2'? O que é '0.15'? Números mágicos sem semântica.
        if (perfilCliente == 2) {
            return valorTotal - (valorTotal * 0.15);
        }
        
        // PROBLEMA: String mágica "CANCELADO" avaliada diretamente. Suscetível a erros de digitação ou mudanças de case.
        if (perfilCliente == 99) {
            throw new IllegalArgumentException("Cliente com status CANCELADO não pode comprar.");
        }
        return valorTotal;
    }
}
```

## Como Fazer Corretamente

```java
package com.empresa.mvc.service;

public class PedidoService {
    // SOLUÇÃO: Utilização de constantes descritivas na classe para valores numéricos imutáveis
    private static final double DESCONTO_CLIENTE_VIP = 0.15;

    // SOLUÇÃO: Utilização de Enums para consolidar os estados possíveis do domínio
    public enum PerfilCliente {
        COMUM(1),
        VIP(2),
        CANCELADO(99);

        private final int codigo;
        PerfilCliente(int codigo) { this.codigo = codigo; }
        public int getCodigo() { return codigo; }
    }

    public double calcularDesconto(double valorTotal, PerfilCliente perfil) {
        if (perfil == PerfilCliente.VIP) {
            return valorTotal - (valorTotal * DESCONTO_CLIENTE_VIP);
        }
        if (perfil == PerfilCliente.CANCELADO) {
            throw new IllegalArgumentException("Cliente com status CANCELADO não pode efetuar compras.");
        }
        return valorTotal;
    }
}
```
## Impacto da Refatoração

- Rastreabilidade: Encontrar todos os pontos do sistema que aplicam o desconto VIP torna-se apenas uma busca por referências da constante `DESCONTO_CLIENTE_VIP`.

- Prevenção de Erros: O compilador garante que os tipos de PerfilCliente sejam válidos na tipagem, eliminando falhas silenciosas por erros de digitação de strings ou inteiros.