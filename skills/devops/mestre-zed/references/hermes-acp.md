# Hermes no Zed por ACP

ACP é o protocolo que liga a IDE ao agente por mensagens estruturadas sobre entrada/saída padrão.

## Pré-requisito

1. Carregue a skill `hermes-agent` e consulte a documentação oficial atual.
2. Rode `hermes acp --check`.
3. Resolva caminhos absolutos de `hermes` e `HERMES_HOME`.
4. Não copie credenciais para o Zed; Hermes lê seu próprio cofre/configuração.

## Registro manual

Estrutura oficial do Zed:

```json
{
  "agent_servers": {
    "Hermes": {
      "type": "custom",
      "command": "/caminho/absoluto/hermes",
      "args": ["acp"],
      "env": { "HERMES_HOME": "/caminho/do/hermes-home" }
    }
  }
}
```

O processo externo é dono do modelo, autenticação, ferramentas e configuração nativa. Configurar um provedor no Zed Agent não configura Hermes.

## Verificação

1. Reabrir Zed ou confirmar recarga automática do settings.
2. Criar thread do agente externo Hermes pelo seletor.
3. Enviar pedido de leitura não destrutivo no projeto.
4. Confirmar eventos de ferramenta e resposta.
5. Abrir `dev: open acp logs` se o agente não aparecer ou travar.
6. Confirmar novamente `hermes acp --check` fora do Zed.

## Diagnóstico

- Agente ausente: nome/chave inválida, binário não executável ou caminho relativo.
- Sai imediatamente: falha no `--check`, autenticação/modelo ou variável `HERMES_HOME` errada.
- Ferramenta ausente: verificar configuração MCP do Zed e configuração nativa do Hermes; são camadas diferentes.
- Dois agentes editando os mesmos arquivos: interromper um e repetir em worktree separada.

Fontes:
- https://zed.dev/docs/ai/external-agents
- https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration
