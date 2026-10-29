---
name: mestre-zed
description: Use when installing, configuring, or operating Zed IDE.
version: 0.1.0
author: Nícholas Nagaita, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Zed, IDE, ACP, Tasks, LSP]
    related_skills: [hermes-agent]
---

# Mestre Zed

Opera Zed como ambiente de engenharia: instalação, configuração, linguagens, tarefas, Git, agentes externos e diagnóstico. Antes de mudar uma chave, consulta a documentação atual; configuração plausível sem fonte é defeito.

## Quando usar

- Instalar, atualizar, remover ou diagnosticar Zed.
- Editar `settings.json`, `keymap.json`, `.zed/tasks.json` ou `.zed/debug.json`.
- Configurar TypeScript, JavaScript, React, Next.js, Bun, pnpm, Prettier, ESLint ou servidor de linguagem.
- Ligar Hermes ou outro agente externo por ACP.
- Trabalhar com Git, vários agentes ou worktrees no Zed.

Não usar para: decidir arquitetura do produto ou alterar código sem relação com o editor.

## Princípios obrigatórios

1. Descobrir sistema, versão do Zed, raiz do projeto, manifesto e instruções locais antes de editar.
2. Consultar Context7 em duas etapas: `ctx7 library zed "<tema>"`; depois `ctx7 docs /websites/zed_dev "<um conceito>"`.
3. Preferir documentação oficial `https://zed.dev/docs/`; usar o repositório apenas para detalhes ausentes.
4. Não inventar chave, ação, nome de linguagem ou formato JSON. Sem fonte legível: `null` e buscar.
5. Separar configuração global de preferência pessoal da configuração `.zed/` exigida pelo projeto.
6. Nunca colocar segredo em settings, tasks, keymap ou repositório. Referenciar variável de ambiente.
7. Verificar JSON, abrir Zed em primeiro plano, ler logs e executar ao menos uma tarefa real.

## Fluxo de trabalho

1. Leia `references/operacao.md` e apenas as referências ligadas ao pedido.
2. Meça pré-requisitos: versão, arquitetura, biblioteca C, Vulkan/GPU, memória, executáveis e estado Git.
3. Leia instruções do repositório e seus manifestos. Não presuma npm quando há pnpm/Bun.
4. Faça a menor configuração suficiente. Em máquina com pouca memória, limite servidor TypeScript abaixo da RAM física e não abra builds pesados em paralelo.
5. Para Hermes, rode `hermes acp --check` antes de registrar o agente; use caminho absoluto para evitar `PATH` diferente na interface gráfica.
6. Valide JSON e inicie `zed <projeto> --foreground`. Procure erro de configuração, agente, servidor de linguagem e tarefa no log.
7. Execute a tarefa de verificação do projeto. Só declare pronto se o comando real terminou com código zero.

## Referências

- `references/operacao.md`: instalação, arquivos, diagnóstico e fontes.
- `references/configuracao.md`: chaves, linguagens, tarefas, Git e ergonomia.
- `references/hermes-acp.md`: integração Hermes–Zed e verificação.
- `references/context7.md`: conexão do Context7 ao Zed e verificação.

## Erros comuns

- Usar pacote comunitário antigo quando existe instalador oficial.
- Copiar `settings.json` de outra versão e aceitar chaves silenciosamente ignoradas.
- Definir `npm`, `pnpm` ou `bun` sem conferir o gerenciador real.
- Rodar dois formatadores ou dois servidores TypeScript concorrentes.
- Dar 8–16 GiB ao vtsls numa máquina com 7,6 GiB.
- Colocar token em `terminal.env`; esse arquivo não é cofre.
- Confundir Zed Agent com agente externo: autenticação e modelo do externo pertencem ao próprio agente.
- Criar agentes paralelos no mesmo diretório; use worktree quando houver sobreposição de arquivos.

## Verificação de alta

- `zed --version` responde.
- Binário real com `--system-specs` confirma sistema e Vulkan.
- Todos os JSON carregam com parser.
- `hermes acp --check` responde `OK` quando Hermes foi configurado.
- Zed permanece aberto sem erro de configuração no log.
- Uma tarefa do projeto roda de dentro do mesmo diretório e devolve código zero.
- `git status --short` mostra apenas mudanças intencionais.
