# Operação do Zed

## Fonte e atualização

Use um conceito por consulta:

- `ctx7 library zed "IDE settings tasks ACP Linux"`
- `ctx7 docs /websites/zed_dev "Linux installation"`
- `ctx7 docs /websites/zed_dev "settings files precedence"`
- `ctx7 docs /websites/zed_dev "tasks variables cwd"`
- `ctx7 docs /websites/zed_dev "external agents ACP custom agent"`

Índice oficial: https://zed.dev/docs/llms.txt

## Instalação Linux

O instalador oficial estável é `curl -f https://zed.dev/install.sh | sh`. Inspecione o script quando a política local exigir. Requisitos oficiais: GPU compatível com Vulkan; glibc >=2.31 em x86_64 e >=2.35 em aarch64. Preview não é padrão de produção.

Verifique:

- `zed --version`
- executável real retornado pela versão
- `<binário-real> --system-specs`
- `vulkaninfo --summary`
- `~/.local/share/zed/logs/Zed.log`

O comando `zed --system-specs` pode ser apenas o lançador e indicar o caminho do binário real. Siga a mensagem; não trate isso como falha da GPU.

Remoção da instalação oficial: `zed --uninstall`.

## Arquivos

Linux/macOS:

- Global: `~/.config/zed/settings.json`
- Teclas: `~/.config/zed/keymap.json`
- Tarefas globais: `~/.config/zed/tasks.json`
- Projeto: `<raiz>/.zed/settings.json`
- Tarefas do projeto: `<raiz>/.zed/tasks.json`
- Depuração: `<raiz>/.zed/debug.json`

Configuração do projeto complementa/substitui a global. Não grave preferência pessoal no repositório sem necessidade coletiva.

## Diagnóstico

1. Validar JSON/JSONC com parser compatível.
2. Iniciar `zed <raiz> --foreground`.
3. Ler `Zed.log` e buscar `error`, `invalid`, `unknown`, `failed`, nome do agente e servidor de linguagem.
4. Para teclas, usar `dev: open key context view`.
5. Para agentes ACP, usar `dev: open acp logs`.
6. Para linguagem, reiniciar o servidor só após corrigir configuração.
7. Para índice parcial, confirmar se a raiz aberta é o repositório Git; não definir `file_scan_depth: 0` em árvore enorme sem medir custo.

## Fontes oficiais

- Linux: https://zed.dev/docs/linux
- Configuração: https://zed.dev/docs/configuring-zed
- Teclas: https://zed.dev/docs/key-bindings
- Tarefas: https://zed.dev/docs/tasks
- TypeScript: https://zed.dev/docs/languages/typescript
- Telemetria: https://zed.dev/docs/telemetry
- Agentes externos: https://zed.dev/docs/ai/external-agents
