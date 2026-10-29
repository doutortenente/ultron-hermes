# Inventário do Modelo de Dados Canônico SASI v3

## a) Tabelas do modelo canônico (finalidade em 1 linha)

| # | Tabela | Finalidade |
|---|--------|-----------|
| 1 | `evento_tipo_ref` | Dimensão-legenda que governa o vocabulário de `eventos_clinicos.tipo` (unidade, faixa fisiológica, slot LOINC). |
| 2 | `pacientes` | Registro-mestre do leito/paciente: cadastro, status, semáforo de gravidade, dispositivos, riscos e ficha congelada (patient_summary). |
| 3 | `evolucoes` | 1 retrato do plantão por paciente: 7 sistemas em JSONB, DVA/sedativos, impressão↔conduta (1:1), riscos, prescrição, SOFA snapshot. |
| 4 | `eventos_clinicos` | Série temporal: 1 linha por medição, com fonte, confiança e flag `requires_review`. |
| 5 | `atbs` | Antibióticos em uso (stewardship): droga, dose, via, intenção, foco, agente-alvo. |
| 6 | `culturas` | Microbiologia: material, coleta, crecimento, agente, UFC. |
| 7 | `antibiograma` | Relacionamento 1:N com culturas: S/I/R por antibiótico. |
| 8 | `pendencias` | Tarefas/follow-up por paciente (prioridade 1–3, status concluída). |
| 9 | `alerts_log` | Alertas disparados (anti-repetição por hash SHA-256). |
| 10 | `ingest_audit_log` | Auditoria de cada ingestão (OCR/API/batch): payload bruto, resposta, warnings, status. |
| 11 | `memorias` | Store vetorial (pgvector 768d) para RAG — busca semântica de conteúdo. |
| 12 | `alert_rules` | Configuração do motor de alertas por valor (comparador + limiar). |
| 13 | `trend_rules` | Configuração do motor de alertas por tendência (modo, limiar, janela). |

## b) Campos por tabela

### `evento_tipo_ref`
| Campo | Tipo | Enum/Valores | Obrigatório |
|-------|------|--------------|-------------|
| `codigo` | text | PK (ex.: 'fc', 'lactato') | Sim |
| `categoria` | text | 'vital' 'gaso' 'lab' 'renal' 'hemato' 'infecto' 'droga' 'neuro' 'score' 'bh' 'outro' | Sim |
| `rotulo` | text | Descritivo | Sim |
| `unidade_padrao` | text | ex.: 'bpm', 'mmHg', 'mg/dL' | Não |
| `faixa_min` | numeric | Limite fisiológico impossível (inferior) | Não |
| `faixa_max` | numeric | Limite fisiológico impossível (superior) | Não |
| `loinc_code` | text | Código FHIR Observation.code | Não |
| `ativo` | boolean | default true | Sim |
| `ordem` | integer | default 100 | Sim |

### `pacientes`
| Campo | Tipo | Enum/Valores | Obrigatório |
|-------|------|--------------|-------------|
| `id` | uuid | PK, gen_random_uuid() | Sim |
| `user_id` | uuid | FK auth.users(id) | Não |
| `leito` | text | L01..L12 | Sim |
| `uti` | `uti_enum` | 'UTI2','UTI3','UTI4' | Sim |
| `nome` | text | 1–200 chars | Sim |
| `idade` | integer | 0–130 | Não |
| `peso` | numeric(5,2) | 1–400 | Não |
| `altura` | numeric(5,2) | 30–250 (cm) | Não |
| `hd` | text | Hipóteses/problemas ativos | Não |
| `data_adm` | date | default current_date | Sim |
| `alergias` | text | | Não |
| `gravidade` | `gravidade_enum` | 'estavel','moderado','grave','critico','obito' | Sim, default 'estavel' |
| `status_leito` | `status_leito_enum` | 'ativo','alta','obito','transferencia' | Sim, default 'ativo' |
| `sofa_baseline` | integer | 0–24 | Não |
| `isolation` | `isolamento_enum` | 'none','contact','droplet','aerosol' | Sim, default 'none' |
| `out_of_range_count` | integer | default 0 | Sim |
| `severidade_visual` | `severidade_visual_enum` | 'red','yellow','green' | Sim, default 'green' |
| `dispositivos` | jsonb | {iot,cvc,pai,svd,sne,avp,picc,tqt,dreno,mpd,shilley,detalhe} | Sim, default '{}' |
| `riscos_flags` | jsonb | {pav,broncoaspiracao,upp,queda,diabetico} | Sim, default '{}' |
| `patient_summary` | jsonb | Contrato PatientSummary (ver tipos.ts) | Não |
| `imc` | numeric | GERADO (stored) | Derivado |
| `created_at` | timestamptz | default now() | Sim |
| `updated_at` | timestamptz | default now() | Sim |

### `evolucoes`
| Campo | Tipo | Enum/Valores | Obrigatório |
|-------|------|--------------|-------------|
| `id` | uuid | PK | Sim |
| `paciente_id` | uuid | FK pacientes(id) ON DELETE CASCADE | Sim |
| `user_id` | uuid | FK auth.users(id) | Não |
| `data_evolucao` | timestamptz | default now() | Sim |
| `plantao` | `plantao_enum` | 'manha','tarde','noite','plantao_24h' | Sim, default 'manha' |
| `neuro` | jsonb | {descricao, rass} | Sim, default '{}' |
| `resp` | jsonb | {suporte, fr_max, fr_min, spo2_max, spo2_min, obs} | Sim, default '{}' |
| `hemo` | jsonb | {pa_sys_max, pa_sys_min, pa_dia_max, pa_dia_min, pam_max, pam_min, fc_max, fc_min, ritmo, obs} | Sim, default '{}' |
| `tgi` | jsonb | {dieta, obs} | Sim, default '{}' |
| `renal` | jsonb | {cr, ur, diurese_6_18h_ml, bh_6_18h_ml, descricao, obs} | Sim, default '{}' |
| `hemato` | jsonb | {hb, ht, plaq, obs} | Sim, default '{}' |
| `infecto` | jsonb | {atb, tmax, leuco, obs} | Sim, default '{}' |
| `dvas` | jsonb | [{droga, dose, unidade}] | Sim, default '[]' |
| `sedativos` | jsonb | [{droga, dose, unidade}] | Sim, default '[]' |
| `impressao` | text[] | 1 problema por item | Sim, default '{}' |
| `conduta` | text[] | 1:1 com impressao | Sim, default '{}' |
| `problemas_ativos` | jsonb | [{texto, sistema?, gravidade?}] | Sim, default '[]' |
| `condutas_sistemas` | jsonb | [{sistema, texto, meta?, prazo?}] | Sim, default '[]' |
| `riscos` | jsonb | [{texto, nivel?}] | Sim, default '[]' |
| `prescricao` | jsonb | {cardiovascular, snc, gastro_endocrino, infeccioso_resp, sintomaticos_sn, solucoes_diureticos, nutricao} | Não |
| `sofa_snapshot` | jsonb | Cache invalidado por trigger | Derivado |
| `sofa_total` | integer | 0–24 | Derivado |
| `created_at` | timestamptz | default now() | Sim |
| `updated_at` | timestamptz | default now() | Sim |

### `eventos_clinicos`
| Campo | Tipo | Enum/Valores | Obrigatório |
|-------|------|--------------|-------------|
| `id` | uuid | PK | Sim |
| `paciente_id` | uuid | FK pacientes(id) ON DELETE CASCADE | Sim |
| `evolucao_id` | uuid | FK evolucoes(id) ON DELETE SET NULL | Não |
| `user_id` | uuid | FK auth.users(id) | Não |
| `ts` | timestamptz | Timestamp da medição | Sim |
| `tipo` | text | FK evento_tipo_ref(codigo) — 57 códigos canônicos | Sim |
| `valor_num` | numeric | | Não (mas check: valor_num OR valor_json NOT NULL) |
| `valor_json` | jsonb | custom: {dominio, subtipo, unidade}; pf_ratio: {suporte_vent}; ecocardiograma: {indice_cardiaco, rvs, psap, vci_colapsabilidade, feve, tapse, delta_vpeak} | Não |
| `unidade` | text | | Não |
| `fonte` | `fonte_evento_enum` | 'manual','gemini_ocr','claude_ocr','appsheet','auto_trigger','edge_function','api_import' | Sim |
| `confidence` | numeric(3,2) | 0–1 | Não |
| `source_text` | text | Texto original (OCR) | Não |
| `requires_review` | boolean | default false | Sim |
| `created_at` | timestamptz | default now() | Sim |

### `atbs`
| Campo | Tipo | Enum/Valores | Obrigatório |
|-------|------|--------------|-------------|
| `id` | uuid | PK | Sim |
| `paciente_id` | uuid | FK pacientes(id) ON DELETE CASCADE | Sim |
| `user_id` | uuid | FK auth.users(id) | Não |
| `droga` | text | Nome do antibiótico | Sim |
| `dose` | text | | Não |
| `via` | `via_atb_enum` | 'EV','VO','IM','SC','SNE','SNG','IT','Tópico' | Não |
| `frequencia` | text | | Não |
| `data_inicio` | date | default current_date | Sim |
| `data_fim` | date | | Não |
| `intencao` | `intencao_atb_enum` | 'empirica','dirigida','profilatica' | Não |
| `foco` | text | | Não |
| `agente_alvo` | text | | Não |
| `motivo_suspensao` | text | | Não |
| `duracao_planejada_dias` | integer | | Não |
| `created_at` | timestamptz | default now() | Sim |
| `updated_at` | timestamptz | default now() | Sim |

### `culturas`
| Campo | Tipo | Enum/Valores | Obrigatório |
|-------|------|--------------|-------------|
| `id` | uuid | PK | Sim |
| `paciente_id` | uuid | FK pacientes(id) ON DELETE CASCADE | Sim |
| `user_id` | uuid | FK auth.users(id) | Não |
| `material` | `material_cultura_enum` | 'hemocultura','urocultura','aspirado_traqueal','lavado_bal','lcr','secrecao_ferida','liquido_peritoneal','liquido_pleural','outro' | Sim |
| `coleta_ts` | timestamptz | | Sim |
| `laudo_ts` | timestamptz | (check: laudo >= coleta) | Não |
| `crescimento` | boolean | default false | Sim |
| `agente` | text | | Não |
| `ufc_por_ml` | numeric | Unidade formadora de colônias | Não |
| `observacoes` | text | | Não |
| `created_at` | timestamptz | default now() | Sim |
| `updated_at` | timestamptz | default now() | Sim |

### `antibiograma`
| Campo | Tipo | Enum/Valores | Obrigatório |
|-------|------|--------------|-------------|
| `id` | uuid | PK | Sim |
| `cultura_id` | uuid | FK culturas(id) ON DELETE CASCADE | Sim |
| `antibiotico` | text | | Sim |
| `resultado` | `antibiograma_resultado_enum` | 'S','I','R' | Sim |
| `cim` | numeric | Concentração de inibição mínima | Não |
| `created_at` | timestamptz | default now() | Sim |

### `pendencias`
| Campo | Tipo | Enum/Valores | Obrigatório |
|-------|------|--------------|-------------|
| `id` | uuid | PK | Sim |
| `paciente_id` | uuid | FK pacientes(id) ON DELETE CASCADE | Sim |
| `evolucao_id` | uuid | FK evolucoes(id) ON DELETE SET NULL | Não |
| `user_id` | uuid | FK auth.users(id) | Não |
| `tarefa` | text | 1–500 chars | Sim |
| `prioridade` | smallint | 1 (alta)–3 (baixa), default 2 | Sim |
| `concluida` | boolean | default false | Sim |
| `concluida_at` | timestamptz | | Não |
| `created_at` | timestamptz | default now() | Sim |

### `alerts_log`
| Campo | Tipo | Enum/Valores | Obrigatório |
|-------|------|--------------|-------------|
| `id` | uuid | PK | Sim |
| `paciente_id` | uuid | FK pacientes(id) ON DELETE CASCADE | Sim |
| `evento_id` | uuid | FK eventos_clinicos(id) ON DELETE SET NULL | Não |
| `user_id` | uuid | FK auth.users(id) | Não |
| `tipo` | text | Rótulo da regra disparada | Sim |
| `severidade` | `severidade_alerta_enum` | 'info','warning','critical' | Sim, default 'warning' |
| `mensagem` | text | Template com {v}/{prev}/{d} preenchido | Sim |
| `payload` | jsonb | Contexto do alerta | Não |
| `hash_key` | text | SHA-256 do alerta (dedup) | Sim |
| `acked` | boolean | default false | Sim |
| `acked_at` | timestamptz | | Não |
| `acked_by` | uuid | FK auth.users(id) (quem reconheceu) | Não |
| `created_at` | timestamptz | default now() | Sim |

### `ingest_audit_log`
| Campo | Tipo | Enum/Valores | Obrigatório |
|-------|------|--------------|-------------|
| `id` | uuid | PK | Sim |
| `user_id` | uuid | FK auth.users(id) | Não |
| `paciente_id` | uuid | FK pacientes(id) ON DELETE SET NULL | Não |
| `source_type` | text | Tipo da fonte (ex.: 'ocr', 'api') | Não |
| `fonte` | text | Fonte específica (ex.: 'claude_ocr') | Não |
| `payload_raw` | jsonb | Envelope bruto original | Não |
| `response` | jsonb | Resposta da ingestão | Não |
| `eventos_ids` | uuid[] | IDs de eventos criados | Não |
| `warnings` | text[] | Avisos da ingestão | Não |
| `ok` | boolean | Sucesso da ingestão | Sim |
| `error_msg` | text | Mensagem de erro se falhou | Não |
| `created_at` | timestamptz | default now() | Sim |

### `memorias`
| Campo | Tipo | Enum/Valores | Obrigatório |
|-------|------|--------------|-------------|
| `id` | bigint | PK, identity | Sim |
| `user_id` | uuid | FK auth.users(id) ON DELETE CASCADE | Não |
| `conteudo` | text | Texto da memória | Sim |
| `metadata` | jsonb | Metadados (tags, source, etc.) | Não |
| `embedding` | `extensions.vector(768)` | Vetor de embedding (pgvector) | Não |
| `created_at` | timestamptz | default now() | Não |

### `alert_rules`
| Campo | Tipo | Enum/Valores | Obrigatório |
|-------|------|--------------|-------------|
| `id` | uuid | PK | Sim |
| `ativo` | boolean | default true | Sim |
| `tipo_evento` | text | FK evento_tipo_ref(codigo) | Sim |
| `comparador` | `comparador_enum` | 'lt','lte','gt','gte' | Sim |
| `limiar` | numeric | | Sim |
| `severidade` | `severidade_alerta_enum` | 'info','warning','critical' | Sim |
| `rotulo` | text | unique | Sim |
| `mensagem` | text | | Sim |
| `fonte` | text | | Não |
| `ordem` | integer | default 100 | Sim |
| `created_at` | timestamptz | default now() | Sim |

### `trend_rules`
| Campo | Tipo | Enum/Valores | Obrigatório |
|-------|------|--------------|-------------|
| `id` | uuid | PK | Sim |
| `ativo` | boolean | default true | Sim |
| `tipo_evento` | text | FK evento_tipo_ref(codigo) | Sim |
| `modo` | `trend_modo_enum` | 'subida_abs','subida_rel','queda_abs' | Sim |
| `limiar` | numeric | | Sim |
| `janela_max_horas` | integer | | Não |
| `severidade` | `severidade_alerta_enum` | 'info','warning','critical' | Sim |
| `rotulo` | text | unique | Sim |
| `mensagem` | text | | Sim |
| `fonte` | text | | Não |
| `ordem` | integer | default 100 | Sim |
| `created_at` | timestamptz | default now() | Sim |

## c) Relações entre tabelas

```text
pacientes ||--o{ evolucoes          (cascade)
pacientes ||--o{ eventos_clinicos    (cascade)
pacientes ||--o{ pendencias          (cascade)
pacientes ||--o{ atbs                (cascade)
pacientes ||--o{ culturas            (cascade)
pacientes ||--o{ alerts_log          (cascade)
pacientes ||--o{ memorias            (dono via user_id)
culturas  ||--o{ antibiograma        (cascade)
evolucoes ||--o{ eventos_clinicos     (set null)
evento_tipo_ref ||--o{ eventos_clinicos   (FK tipo)
evento_tipo_ref ||--o{ alert_rules         (FK tipo_evento)
evento_tipo_ref ||--o{ trend_rules         (FK tipo_evento)
eventos_clinicos ||--o{ alerts_log         (evento_id opcional)
```

## d) Campos DERIVADOS (calculados por trigger/view — nunca escritos manualmente)

| Campo | Fonte | Mecanismo |
|-------|-------|-----------|
| `pacientes.imc` | `peso / ((altura/100)²)` | Coluna gerada `stored` |
| `pacientes.severidade_visual` | `gravidade` | Trigger `sync_severidade_visual` (UPDATE) + trigger `trg_severidade_on_insert` (INSERT — nova no v3) |
| `pacientes.out_of_range_count` | eventos fora da faixa fisiológica | Trigger `fn_invalidate_sofa_cache` (implícito — contagem por triggers) |
| `evolucoes.sofa_snapshot` | JSONB dos 6 componentes do SOFA (resp, coag, liver, cardio, neuro, renal) | Invalidado (set null) pelo trigger `fn_invalidate_sofa_cache` quando sistemas/DVA/sedativos mudam |
| `evolucoes.sofa_total` | Soma dos 6 SOFA components | Invalidado pelo mesmo trigger; recalculado fora do banco |
| `*_24h`, `*_48h`, `*_72h` | Balanço hídrico acumulado | View `vw_bh_acumulado` (soma de eventos `bh_h` em janelas) |
| `dias_internacao` | `current_date - data_adm` | View `vw_dashboard_uti` |
| `delta_sofa_24h` | `sofa_total (atual) - sofa_total (24h atrás)` | View `vw_dashboard_uti` |
| `pendencias_abertas` | COUNT das pendências não concluídas | View `vw_dashboard_uti` |
| `stewardship_flag` | `dias_terapia` (dias ativos do atb) | View `vw_dias_atb_ativo` (>14: critical, >7: warning, senão: ok) |
| `dias_terapia` | `current_date - data_inicio + 1` | View `vw_dias_atb_ativo` |
| `valor_anterior`, `delta`, `gap_horas` | `LAG()` sobre eventos do mesmo tipo/paciente | View `vw_eventos_tendencia` |
| `sofa_total_24h` | Último `sofa_total` evento ≤ 24h atrás | View `vw_dashboard_uti` (CTE `sofa_24h_atras`) |
| `ultima_evolucao` | Última evolução por paciente | View `vw_dashboard_uti` (CTE `ultima_evol`) |

## e) Vocabulário completo de tipos de evento clínico (códigos canônicos em `evento_tipo_ref`)

### Vitais (9)
| Código | Rótulo | Unidade | Faixa min/max | LOINC |
|--------|--------|---------|---------------|-------|
| `pa_sys` | PA sistólica | mmHg | 40–280 | 8480-6 |
| `pa_dia` | PA diastólica | mmHg | 20–160 | 8462-4 |
| `pam` | PA média | mmHg | 30–180 | — |
| `pam_min` | PA média (mínima) | mmHg | 30–180 | — |
| `fc` | Frequência cardíaca | bpm | 20–250 | 8867-4 |
| `fr` | Frequência respiratória | ipm | 4–80 | — |
| `spo2` | Saturação O2 | % | 0–100 | 2708-6 |
| `temp` | Temperatura | °C | 32–42 | 8310-5 |
| `glicemia` | Glicemia capilar (Dx) | mg/dL | 20–800 | — |

### Gasometria (6)
| Código | Rótulo | Unidade | Faixa min/max | LOINC |
|--------|--------|---------|---------------|-------|
| `pf_ratio` | Relação PaO2/FiO2 | — | 50–600 | — |
| `lactato` | Lactato | mmol/L | 0.5–25 | — |
| `ph` | pH arterial | — | 6.80–7.80 | — |
| `pco2` | pCO2 | mmHg | 10–150 | — |
| `po2` | pO2 | mmHg | 20–600 | — |
| `hco3` | Bicarboneto | mEq/L | 4–50 | — |
| `be` | Base excess | mEq/L | — (null) | — |

### Renal (7)
| Código | Rótulo | Unidade | Faixa min/max | LOINC |
|--------|--------|---------|---------------|-------|
| `diurese_h` | Diurese horária | mL/h | — | — |
| `bh_h` | Balanço hídrico horário | mL | — | — |
| `bh_acumulado` | Balanço hídrico acumulado | mL | — | — |
| `cr` | Creatinina | mg/dL | 0.1–20 | — |
| `ur` | Ureia | mg/dL | 5–400 | — |
| `na` | Sódio | mEq/L | 110–180 | — |
| `k` | Potássio | mEq/L | 1.5–9.5 | — |
| `mg` | Magnésio | mg/dL | — | — |
| `ca` | Cálcio | mg/dL | — | — |
| `p` | Fósforo | mg/dL | — | — |

### Hematologia (6)
| Código | Rótulo | Unidade | Faixa min/max | LOINC |
|--------|--------|---------|---------------|-------|
| `hb` | Hemoglobina | g/dL | 2–22 | — |
| `ht` | Hematócrito | % | — | — |
| `plaq` | Plaquetas | ×10³/µL | 1–2000 | — |
| `leuco` | Leucócitos | ×10³/µL | 0.1–100 | — |
| `inr` | INR | — | 0.8–10 | — |

### Infeccioso/Fígado (3)
| Código | Rótulo | Unidade | Faixa min/max | LOINC |
|--------|--------|---------|---------------|-------|
| `bb` | Bilirrubina total | mg/dL | — | — |
| `pcr` | Proteína C reativa | mg/L | — | — |
| `procalcitonina` | Procalcitonina | ng/mL | — | — |

### Drogas (9)
| Código | Rótulo | Unidade | Faixa min/max | LOINC |
|--------|--------|---------|---------------|-------|
| `nor_dose` | Noradrenalina (dose) | mcg/kg/min | 0.001–2.0 | — |
| `adr_dose` | Adrenalina (dose) | mcg/kg/min | 0.001–2.0 | — |
| `vaso_dose` | Vasopressina (dose) | U/min | 0.01–0.1 | — |
| `dobuta_dose` | Dobutamina (dose) | mcg/kg/min | 0–30 | — |
| `dopa_dose` | Dopamina (dose) | mcg/kg/min | 0–30 | — |
| `fent_dose` | Fentanil (dose) | mcg/h | — | — |
| `midaz_dose` | Midazolam (dose) | mg/h | — | — |
| `propofol_dose` | Propofol (dose) | mcg/kg/min | — | — |
| `precedex_dose` | Dexmedetomidina (dose) | mcg/kg/h | — | — |

### Neuro (5)
| Código | Rótulo | Unidade | Faixa min/max | LOINC |
|--------|--------|---------|---------------|-------|
| `gcs` | Escala de coma de Glasgow | — | 3–15 | — |
| `rass` | RASS | — | -5–4 | — |
| `cam_icu` | CAM-ICU | — | — | — |
| `bps` | Behavioral Pain Scale | — | — | — |
| `cpot` | CPOT | — | — | — |

### SOFA (7)
| Código | Rótulo | Unidade | Faixa min/max | LOINC |
|--------|--------|---------|---------------|-------|
| `sofa_total` | SOFA total | — | 0–24 | — |
| `sofa_resp` | SOFA respiratório | — | 0–4 | — |
| `sofa_coag` | SOFA coagulação | — | 0–4 | — |
| `sofa_liver` | SOFA hepático | — | 0–4 | — |
| `sofa_cardio` | SOFA cardiovascular | — | 0–4 | — |
| `sofa_neuro` | SOFA neurológico | — | 0–4 | — |
| `sofa_renal` | SOFA renal | — | 0–4 | — |

### Custom/livre (1)
| Código | Rótulo | Unidade | Faixa min/max | LOINC |
|--------|--------|---------|---------------|-------|
| `custom` | Livre — eco/hemodinâmica/imagem/cultura via `valor_json {dominio,subtipo,unidade}` | — | — | — |

**Total: 56 códigos canônicos + 1 (`custom`) = 57 linhas na dimensão.**

## f) Enums formais (14 tipos citados no design)

| Enum | Schema | Valores |
|------|--------|---------|
| `uti_enum` | public | 'UTI2','UTI3','UTI4' |
| `gravidade_enum` | public | 'estavel','moderado','grave','critico','obito' |
| `status_leito_enum` | public | 'ativo','alta','obito','transferencia' |
| `isolamento_enum` | public | 'none','contact','droplet','aerosol' |
| `severidade_visual_enum` | public | 'red','yellow','green' |
| `plantao_enum` | public | 'manha','tarde','noite','plantao_24h' |
| `via_atb_enum` | public | 'EV','VO','IM','SC','SNE','SNG','IT','Tópico' |
| `intencao_atb_enum` | public | 'empirica','dirigida','profilatica' |
| `material_cultura_enum` | public | 'hemocultura','urocultura','aspirado_traqueal','lavado_bal','lcr','secrecao_ferida','liquido_peritoneal','liquido_pleural','outro' |
| `antibiograma_resultado_enum` | public | 'S','I','R' |
| `severidade_alerta_enum` | public | 'info','warning','critical' |
| `fonte_evento_enum` | public | 'manual','gemini_ocr','claude_ocr','appsheet','auto_trigger','edge_function','api_import' |
| `comparador_enum` | public | 'lt','lte','gt','gte' |
| `trend_modo_enum` | public | 'subida_abs','subida_rel','queda_abs' |

**Observação:** `gravidade_enum` e `status_leito_enum` já existiam no banco vivo (texto solto + CHECK); as demais 12 são novas no v3.

## g) Regras de negócio que afetam estrutura

### R1 — Carimbo de `severidade_visual` por trigger
- **Trigger `trg_sync_severidade_visual` (UPDATE)**: quando `gravidade` muda E `severidade_visual` não foi manualmente alterada, ajusta automaticamente:
  - `'critico'` → `'red'`
  - `'grave'` → `'red'`
  - `'moderado'` → `'yellow'`
  - demais → `'green'`
- **Trigger `trg_severidade_on_insert` (INSERT)** — **nova no v3 (Anexo B, passo A6)**: o mesmo carimbo aplica no INSERT. Achado corrigido: antes, um paciente admitido como "grave" nascia com `green` até a primeira edição.
- **Consequência para Airtable**: `severidade_visual` é derivado; se `gravidade` for editada, o semáforo deve recalcula automaticamente (não confiar no valor gravado).

### R2 — Invalidação do cache de SOFA
- **Trigger `trg_sofa_cache_invalidate` (UPDATE em evolucoes)**: se qualquer sistema JSONB (`resp`, `hemo`, `renal`, `hemato`, `tgi`, `neuro`) ou `dvas`/`sedativos` mudar, seta `new.sofa_snapshot = null` e `new.sofa_total = null`.
- **Consequência**: `sofa_total` e `sofa_snapshot` em `evolucoes` são sempre recalculados externamente (pelo `clinical-engine`) após invalidação.

### R3 — Auto-marcação de baixa confiança
- **Trigger `trg_autoflag_lowconf` (INSERT em eventos_clinicos)**: se `confidence IS NULL OR confidence < 0.7`, seta `requires_review = true`.
- **Consequência**: eventos de OCR com confiança baixa entram automaticamente na fila de revisão (`vw_eventos_pendentes_revisao`).

### R4 — Motor de alertas (trigger after INSERT em eventos_clinicos)
- **Trigger `trg_eval_alert`**: após inserir um evento, percorre `alert_rules` (ativas, do mesmo `tipo_evento`) e aplica o `comparador` + `limiar`. Se bate, insere em `alerts_log` com hash SHA-256 (`fn_alert_hash`) para deduplicação (`ON CONFLICT (hash_key) DO NOTHING`).
- **Trigger `trg_eval_trend`**: mesma lógica mas para `trend_rules` (modo `subida_abs`/`subida_rel`/`queda_abs`, com janela opcional `janela_max_horas`), usando o valor anterior via `LAG()`.
- **Trava ZERO ALUCINAÇÃO**: não dispara se `requires_review = true` ou `confidence < 0.7` — só age sobre dados confiáveis.

### R5 — Dispositivos derivado (JSONB estruturado, não tabela)
- `pacientes.dispositivos` é um JSONB com chaves booleanas fixas: `{iot, cvc, pai, svd, sne, avp, pico, tqt, dreno, mpd, shilley}` + `detalhe: text`.
- **Não é uma tabela separada** — é um campo denormalizado. Para Airtable, modelar como um campo de checkbox múltiplo ou lookup.

### R6 — `imc` gerado automaticamente
- Coluna `GENERATED ALWAYS AS` (stored): `round(peso / ((altura/100)²), 1)`.
- Atualiza sozinha quando `peso` ou `altura` mudam. Nunca escrito manualmente.

### R7 — Unicidade de leito ativo
- Índice parcial: `uq_pacientes_leito_ativo` sobre `(uti, leito) WHERE status_leito = 'ativo'`.
- Garante 1 paciente ativo por leito/uti. Pacientes com `status_leito IN ('alta','obito','transferencia')` não contam.

### R8 — `internalizacao_id` carimbado por trigger
- **Não existe no schema v3.** O documento de design menciona "internação_id carimbado por trigger" como exemplo ilustrativo de regra de negócio, mas a coluna `data_adm` em `pacientes` já serve como indicador de internação. Esse é um **achado não implementado** — não há trigger carimbando um `internacao_id`.

### R9 — Contract de escrita atômico (`save_ficha`)
- RPC `save_ficha(p_paciente_id, p_pac, p_evol, p_evolucao_id, p_plantao, p_pendencias)` grava `pacientes` + `evolucoes` + `pendencias` em uma única transação (atômico — tudo ou nada).
- Carrega `user_id` via `auth.uid()` (SECURITY DEFINER) e respeita guarda de dono (`user_id IS NULL OR user_id = v_uid`).

### R10 — RLS por dono (produção)
- 4 policies por tabela-filha (`SELECT/INSERT/UPDATE/DELETE`), todas usando `fn_owns_paciente(paciente_id)`.
- `pacientes` e `memorias`: escopo direto `auth.uid() = user_id`.
- `ingest_audit_log`: escopo direto `auth.uid() = user_id` (apenas SELECT/INSERT).
- `alert_rules`, `trend_rules`, `evento_tipo_ref`: leitura aberta para authenticated (não são PHI); escrita apenas por service_role.

### R11 — Faixas de absurdo fisiológico (doutrina)
- `evento_tipo_ref.faixa_min/faixa_max` guardam limites **impossíveis** (hard flag), da skill `03-clinical-sanity-checks.md`.
  - Ex.: SpO₂ > 100 → `physiological_error`; SpO₂ 95–100 → `review` (mais fino, na skill).
- A camada de "review" (ex.: FR > 60) vive na skill de extração, não no banco — o banco apenas marca o impossível.

### R12 — Contrato de ingestão único (`sasi-ocr-ingest/v1`)
- Toda entrada (foto, PDF, laudo, texto) passa por um envelope JSON com: `source` (tipo/fonte/confiança/warnings), `target` (uti/leito/paciente), `paciente_upsert?`, `evolucao_snapshot?`, `eventos_clinicos[]`, `pendencias[]`.
- `ingest_audit_log` registra sempre: rastro obrigatório de cada ingestão.

### R13 — Extensões isoladas
- `pgcrypto`, `pg_trgm`, `vector` criados no schema `extensions`, não em `public`.
- `memorias.embedding` usa `extensions.vector(768)` (pgvector).

---

## Arquivos consultados

1. `/home/dr/vaults/celebro/.../SASI-V2v3/2026-07-30-modelo-dados-v3-design.md` — documento de design (F0)
2. `/home/dr/vaults/celebro/.../SASI-V2v3/Planos de migração-sasi/PLANO-SASI-v3.md` — plano de migração detalhado
3. `/home/dr/vaults/celebro/.../SASI-V2v3/Planos de migração-sasi/plano-sasi-V3.2` — versão 3.2 do plano (com atualização de status: F3/F4/F5 fora de escopo)
4. `/home/dr/vaults/celebro/.../SASI-V2v3/SASIv3planoeanexos/10_schema_producao_v3.sql` — schema de produção do zero (13 tabelas, 7 views, 14 enums, 41 policies, 9 triggers)
5. `/home/dr/vaults/celebro/.../SASI-V2v3/SASIv3planoeanexos/11_migracao_do_vivo.sql` — migração do banco vivo (delta)
6. `/home/dr/vaults/celebro/.../SASI-V2v3/SASIv3planoeanexos/database.types.ts` — tipos TypeScript + contratos JSONB
7. `/home/dr/vaults/celebro/.../SASI-V2v3/SASIv3planoeanexos/LEIA-ME.md` — readme do pacote
8. `/home/dr/vaults/celebro/.../arquivos-sasi/sasi-planilhas-antigas/molde-planilha-sasi-v2.1-supabase.sql` — molde SQL V2.1 (anterior, para referência de contratos JSONB)
9. `/home/dr/vaults/celebro/.../arquivos-sasi/sasi-planilhas-antigas/planilha-uti-estrutura-v1.md` — estrutura da planilha antiga (v1, legado)

## Arquivos faltantes citados mas não encontrados

- `supabase/migrations/2026073012000{0,1,2}_*.sql` — mencionado no design (§2) como as 3 migrations ativas. **Não localizado**.
- `docs/RUNBOOK-migracao-v3.md` — mencionado no design (§2). **Não localizado**.
- `supabase/schema-producao-v3.sql` — mencionado no design (§2) como referência. **Não localizado** (presumivelmente é `10_schema_producao_v3.sql`).
- `supabase/types/sasi.types.ts` — mencionado no design (§2). **Não localizado** (presumivelmente é `database.types.ts`).
- `_SASI_TEMPLATE_BASE_v2.md` — doutrina de faixas fisiológicas. **Não localizado**.
- `sasi-ingest-export/references/03-clinical-sanity-checks.md` — fonte operacional das faixas de absurdo. **Não localizado**.
- `docs/PLANO-SASI-v3.html` — versão HTML navegável do plano. **Não localizado** (apenas `.md`).
- `starter-next/` — esqueleto Next.js 15. **Não localizado** nos caminhos fornecidos.
- **Anexo D** (mapa FHIR completo) — mencionado como existente mas **não localizado** em arquivos.