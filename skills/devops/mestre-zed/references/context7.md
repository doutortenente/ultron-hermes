# Context7 no Zed

## Função

Context7 entrega documentação atual de bibliotecas ao agente dentro do Zed. A conexão usa MCP — o encaixe padronizado entre o editor e ferramentas externas.

## Configuração recomendada

Use o servidor remoto oficial com autenticação pelo navegador, sem gravar chave no `settings.json`:

```json
"context_servers": {
  "context7": {
    "url": "https://mcp.context7.com/mcp/oauth"
  }
}
```

O endereço sem login pelo navegador é `https://mcp.context7.com/mcp` e pode receber `Authorization: Bearer ...`; não use essa forma no arquivo quando o login pelo navegador resolve sem segredo persistido.

## Verificação

1. Validar `~/.config/zed/settings.json` como JSON.
2. Confirmar que o servidor aceita uma mensagem `initialize` e devolve `protocolVersion` e `serverInfo`.
3. Abrir Zed → Settings → AI → MCP Servers → `context7`.
4. Concluir o login no navegador quando solicitado.
5. Confirmar indicador verde com `Server is active`.
6. Abrir uma conversa nova e pedir explicitamente: `use Context7 para consultar a documentação atual do Zed sobre MCP`.
7. Só declarar integração completa após uma ferramenta do Context7 responder dentro do Zed.

## Fontes oficiais

- https://zed.dev/docs/ai/mcp
- https://context7.com/docs/resources/all-clients
