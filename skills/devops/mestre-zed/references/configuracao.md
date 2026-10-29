# Configuração operacional

## Ergonomia sem distração

Para TDAH/dislexia, comece com fonte 16–18, altura confortável, linha atual destacada, quebra limitada, minimapa oculto, animação reduzida, cursor sem piscar e barra vertical visível. São ponto de partida, não diagnóstico médico; ajuste pela leitura real.

Chaves oficiais úteis:

- `base_keymap`: Zed, VSCode, JetBrains, Atom, SublimeText, TextMate, Emacs, Cursor ou None.
- `buffer_font_size`, `ui_font_size`, `agent_font_size`.
- `buffer_line_height`: `standard`, `comfortable` ou valor customizado.
- `preferred_line_length`, `soft_wrap`, `current_line_highlight`.
- `reduce_motion`, `cursor_blink`, `minimap`, `scrollbar`.
- `telemetry.metrics` e `telemetry.diagnostics`.
- `show_edit_predictions`; para desligar o provedor, `edit_predictions.provider: "none"`.

Segredos já entram nos globs padrão de previsão, mas adicione padrões locais como `**/cofre.env`. Não avalie nem envie feedback de conversa que contenha informação sensível.

## TypeScript e JavaScript

Zed traz suporte nativo e usa vtsls por padrão. Prettier é o formatador padrão para TypeScript. Evite trocar para outro servidor sem erro medido.

Em máquina de 7,6 GiB, `maxTsServerMemory: 3072` é limite prudente; o padrão documentado de 8192 pode esgotar a máquina. Isso é orçamento máximo, não reserva imediata.

Se combinar Prettier e ESLint, defina a ordem conscientemente. Não use ESLint como segundo formatador por hábito. O comando de CI do projeto continua sendo a verdade.

## Tarefas

Formato: lista JSON de objetos com `label`, `command`, `args`, `cwd`, `save`, `reveal`, `hide`, `allow_concurrent_runs` e `use_new_terminal`.

Use executável absoluto quando Zed gráfico não herda o mesmo `PATH`. Use `args` separados para caminhos/valores, especialmente quando há espaços. Variáveis oficiais incluem:

- `$ZED_WORKTREE_ROOT`
- `$ZED_MAIN_GIT_WORKTREE`
- `$ZED_FILE`, `$ZED_RELATIVE_FILE`, `$ZED_DIRNAME`
- `$ZED_SELECTED_TEXT`, `$ZED_LANGUAGE`, `$ZED_SYMBOL`

Tarefas são comandos; trate qualquer alteração destrutiva como seria tratada no terminal. Não embuta token em `env`.

## Git e agentes paralelos

`git.worktree_directory` define onde o Zed cria worktrees. Worktree é uma segunda sala do mesmo repositório: cada agente edita sem pisar no arquivo do outro. Não crie worktree se os agentes apenas leem; crie quando podem editar os mesmos caminhos.

Antes: `git status --short --branch`. Depois: revisar diff e rodar testes. Nunca force-push/rebase em repositório que proíbe reescrever histórico.
