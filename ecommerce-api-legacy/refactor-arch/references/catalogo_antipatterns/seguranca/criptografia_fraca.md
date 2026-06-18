# Anti-pattern: Criptografia Fraca
**Linguagem de Exemplo:** Java

## Descrição
Utilizar algoritmos obsoletos como MD5 ou SHA-1 para hashes de integridade/senhas, ou cifras como DES para criptografia simétrica. Esses algoritmos possuem vulnerabilidades severas de colisão conhecidas e podem ser quebrados rapidamente por poder computacional moderno.

## Como NÃO Fazer
```java
package com.empresa.mvc.util;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class HashUtils {
    public static String gerarHashObsoleto(string texto) {
        try {
            // PROBLEMA: MD5 é considerado quebrado e inseguro para sistemas modernos
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] array = md.digest(texto.getBytes());
            StringBuilder sb = new StringBuilder();
            for (byte b : array) {
                sb.append(Integer.toHexString((b & 0xFF) | 0x100).substring(1, 3));
            }
            return sb.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }
}
```

## Como Fazer Corretamente
```java
package com.empresa.mvc.util;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.nio.charset.StandardCharsets;

public class HashUtils {
    public static String gerarHashSeguro(String texto) {
        try {
            // SOLUÇÃO: Utilização de SHA-256 (mínimo recomendado para verificações de integridade não-interativas)
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hashBytes = digest.digest(texto.getBytes(StandardCharsets.UTF_8));
            
            StringBuilder sb = new StringBuilder();
            for (byte b : hashBytes) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) sb.append('0');
                sb.append(hex);
            }
            return sb.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new IllegalStateException("Algoritmo de criptografia configurado incorretamente", e);
        }
    }
}
```

## Impacto da Refatoração
- Confiabilidade: Elimina colisões criptográficas previsíveis.

- Modernização: Enquadra o sistema nos padrões exigidos por bibliotecas de segurança de arquitetura corporativa.