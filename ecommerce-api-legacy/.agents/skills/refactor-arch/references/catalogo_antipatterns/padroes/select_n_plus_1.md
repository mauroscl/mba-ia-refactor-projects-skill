# Anti-pattern: SELECT N+1
**Linguagem de Exemplo:** Java / Python

## Descrição
O problema do SELECT N+1 ocorre quando o sistema executa uma consulta inicial para trazer uma lista de registros (1 query) e, em seguida, dispara uma nova consulta para cada registro retornado da lista (N queries) para carregar relacionamentos. Isso sobrecarrega o banco de dados com chamadas de rede repetitivas.

# Abordagem 1: Problema Implicito via ORM (Java / Hibernate)
## Como não fazer
```java
package com.empresa.mvc.dao;

import jakarta.persistence.EntityManager;
import java.util.List;

public class PedidoDao {
    private EntityManager em;

    public List<Pedido> listarPedidosCadastrados() {
        // PROBLEMA: Carrega os pedidos. Mas se a propriedade Cliente for LAZY, 
        // o Hibernate disparará um novo SELECT para cada cliente ao ler a lista no loop externo.
        return em.createQuery("SELECT p FROM Pedido p", Pedido.class).getResultList();
    }
}
```
## Como Fazer Corretamente
```java
package com.empresa.mvc.dao;

import jakarta.persistence.EntityManager;
import java.util.List;

public class PedidoDao {
    private EntityManager em;

    public List<Pedido> listarPedidosCadastradosRefatorado() {
        // SOLUÇÃO: Utilização de JOIN FETCH para trazer o relacionamento de forma adiantada (Eager) em uma única query SQL
        String jpql = "SELECT p FROM Pedido p JOIN FETCH p.cliente";
        return em.createQuery(jpql, Pedido.class).getResultList();
    }
}
```

# Abordagem 2: Problema Explicito via Loop Query (Python / Raw SQL)
## Como NÃO Fazer
```python
def obter_relatorio_produtos_e_categorias(cursor):
    # PROBLEMA: 1 SELECT inicial para pegar os produtos
    cursor.execute("SELECT id, nome, categoria_id FROM produtos")
    produtos = cursor.fetchall()
    
    relatorio = []
    for prod in produtos:
        prod_id, nome, cat_id = prod
        # N SELECTs executados sequencialmente dentro do laço de repetição
        cursor.execute("SELECT nome_categoria FROM categorias WHERE id = %s", (cat_id,))
        cat_nome = cursor.fetchone()[0]
        relatorio.append({"produto": nome, "categoria": cat_nome})
        
    return relatorio
```

## Como fazer corretamente
```python
def obter_relatorio_produtos_e_categorias_refatorado(cursor):
    # SOLUÇÃO: Execução de uma única instrução JOIN delegando a união de dados ao banco de dados
    query = \"\"\"
        SELECT p.nome, c.nome_categoria 
        FROM produtos p
        INNER JOIN categorias c ON p.categoria_id = c.id
    \"\"\"
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    return [{"produto": linha[0], "categoria": linha[1]} for linha in resultados]
```

## Impacto da Refatoração
- Economia Imediata de Rede: Reduz o tráfego de dados e latência de rede eliminando centenas de conexões espúrias.

- Otimização de Infraestrutura: Alivia o consumo de CPU e locks de tabelas no cluster de banco de dados de produção.