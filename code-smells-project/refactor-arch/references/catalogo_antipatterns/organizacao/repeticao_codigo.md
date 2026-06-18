# Anti-pattern: Repetição de Código
**Linguagem de Exemplo:** Java

## Descrição
Duplicar o mesmo trecho de algoritmo ou regra de cálculo em múltiplos arquivos ou camadas do sistema. A duplicação amplia o esforço de manutenção, visto que correções de bugs precisam ser replicadas manualmente em todos os pontos afetados.


## Como NÃO Fazer

```java
package com.empresa.mvc.service;

public class CalculadoraImpostoService {
    // PROBLEMA: Trecho idêntico de computação de alíquota repetido em classes de serviços distintas
    public double calcularTaxaParaProdutoNacional(double precoBase) {
        double icms = precoBase * 0.18;
        double pis = precoBase * 0.0165;
        double cofins = precoBase * 0.076;
        return precoBase + icms + pis + cofins;
    }
}

// Em outro arquivo: OrderService.java
// public double processarPrecoPedido(double valor) {
//     double icms = valor * 0.18;
//     double pis = valor * 0.0165;
//     double cofins = valor * 0.076;
//     return valor + icms + pis + cofins;
// }

```

## Como fazer corretamente

```java

package com.empresa.mvc.strategy;

// SOLUÇÃO: Extração da regra compartilhada para uma estrutura unificada ou utilitário coeso
public class TributacaoNacionalStrategy {
    private static final double ALIQUOTA_ICMS = 0.18;
    private static final double ALIQUOTA_PIS = 0.0165;
    private static final double ALIQUOTA_COFINS = 0.076;

    public static double aplicarImpostoTotal(double precoBase) {
        double icms = precoBase * ALIQUOTA_ICMS;
        double pis = precoBase * ALIQUOTA_PIS;
        double cofins = precoBase * ALIQUOTA_COFINS;
        return precoBase + icms + pis + cofins;
    }
}

// Reuso desimpedido nas demais classes da aplicação:
// double precoFinalProduto = TributacaoNacionalStrategy.aplicarImpostoTotal(precoBase);
// double precoFinalPedido  = TributacaoNacionalStrategy.aplicarImpostoTotal(valorPedido);

```

## Impacto da Refatoração
- Ponto Único de Verdade: Alterações futuras nas alíquotas do governo necessitam de modificação em apenas um local do código fonte.

- Consistência: Garante que o cálculo seja executado de forma idêntica em toda a plataforma.