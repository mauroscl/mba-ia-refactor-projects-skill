# Anti-pattern: Dependências Deprecated (Obsoletas)
**Linguagem de Exemplo:** Node.js / TypeScript 

## Descrição
Manter bibliotecas, pacotes de terceiros ou módulos nativos que foram marcados como deprecated (obsoletos) pelos seus mantenedores. Bibliotecas descontinuadas param de receber patches de segurança e atualizações de performance, abrindo brechas críticas de exploração e dificultando a atualização das versões da própria linguagem de base.

## Como NÃO fazer
```typescript
import * as request from 'request'; // PROBLEMA: A biblioteca 'request' foi depreciada no NPM em 2020.
import * as crypto from 'crypto';

export class PagamentoService {
    public async notificarGateway(payload: any): Promise<void> {
        // PROBLEMA: Utilização de uma dependência defasada que não recebe mais correções de vulnerabilidades
        request.post({
            url: '[https://gateway.pagamento.com/api/v1/notify](https://gateway.pagamento.com/api/v1/notify)',
            json: payload
        }, (error, response, body) => {
            if (error) {
                console.error("Erro na chamada HTTP:", error);
            }
        });
        
        // PROBLEMA: Uso de método nativo depreciado no próprio Node.js 
        // (createCipher foi depreciado por ser inseguro, em prol de createCipheriv)
        const cipher = crypto.createCipher('aes-256-cbc', 'chave_do_sistema');
        let encrypted = cipher.update(payload.documento, 'utf8', 'hex');
        encrypted += cipher.final('hex');
    }
}
```

## Como fazer corretamente
```typescript
import axios from 'axios'; // SOLUÇÃO: Adoção de uma biblioteca HTTP moderna e ativamente mantida.
import * as crypto from 'crypto';

export class PagamentoService {
    public async notificarGateway(payload: any): Promise<void> {
        try {
            // SOLUÇÃO: Substituição pela sintaxe atualizada do Axios (ou a Fetch API nativa)
            await axios.post('[https://gateway.pagamento.com/api/v1/notify](https://gateway.pagamento.com/api/v1/notify)', payload);
        } catch (error) {
            console.error("Erro na chamada HTTP:", error);
        }
        
        // SOLUÇÃO: Transição para o método seguro e suportado pela documentação oficial atual do Node
        const iv = crypto.randomBytes(16);
        const key = crypto.scryptSync('chave_do_sistema', 'salt_aleatorio', 32);
        const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
        
        let encrypted = cipher.update(payload.documento, 'utf8', 'hex');
        encrypted += cipher.final('hex');
    }
}
```

## Impacto da Refatoração
Segurança Contínua: Evita a presença do projeto em relatórios de auditoria de segurança devido a pacotes com vulnerabilidades conhecidas (falhas apontadas por `npm audit` ou CI/CD pipeline).

Compatibilidade: Garante que o projeto possa ser atualizado para versões futuras do runtime (como Node 20 LTS ou 22) sem quebras estruturais.