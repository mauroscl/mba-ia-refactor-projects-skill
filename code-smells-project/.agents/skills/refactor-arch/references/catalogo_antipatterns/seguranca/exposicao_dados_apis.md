# Anti-pattern: Exposição de Dados Sensíveis em APIs
**Linguagem de Exemplo:** Node.js / TypeScript

## Como NÃO Fazer
```typescript
async getUserProfile(req: Request, res: Response) {
    const user = await this.userRepository.findById(req.params.id);
    // PROBLEMA: Retorna todo o objeto, incluindo hash da senha
    res.status(200).json(user);
}
```

## Como Fazer Corretamente
```typescript
interface UserResponseDTO {
    id: string;
    name: string;
    email: string;
}

async getUserProfile(req: Request, res: Response) {
    const user = await this.userRepository.findById(req.params.id);
    // SOLUÇÃO: DTO explícito
    const responseData: UserResponseDTO = { id: user.id, name: user.name, email: user.email };
    res.status(200).json(responseData);
}
```

## Impacto da Refatoração
- Privacidade: Reduz a superfície de ataque ao ocultar estruturas de tabelas e segredos de autenticação.

- Performance: Diminui o payload trafegado na rede removendo bytes desnecessários da resposta.