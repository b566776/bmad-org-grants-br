# Validação EVL-like (nativa do BMAD) no BGb/BMAD

Este módulo inclui uma validação **EVL-like** (inspirada no Epsilon Validation Language), executada **nativamente pelo BMAD** (sem scripts externos).

A ideia é ter um *gate* objetivo antes de avançar para **revisão/submissão/arquivamento**: se houver **erros**, a validação para e você corrige primeiro.

---

## Como executar

Execute a **Fase 5** pelo menu do agente (workflow `workflows/validacao-projeto.yaml`).
O agente deve aplicar as regras EVL-like lendo os arquivos e então gerar `FASE5_VALIDACAO.md`.

---

## Saídas e comportamento de gate

Saída principal:
- `FASE5_VALIDACAO.md` (relatório do gate)

**Gate**:
- Se houver **erros**, o status deve ser **FAIL** e o projeto não deve avançar.
- Avisos não bloqueiam, mas devem ser revisados.

---

## O que é verificado (MVP)

Atualmente o gate cobre:
- **Artefatos obrigatórios presentes**: `FASE1_ANALISE.md`, `FASE2_PLANEJAMENTO.md`, `FASE3_SOLUCAO.md`, `FASE4_IMPLEMENTACAO.md`, `TEMPLATE_PROJETO_EDITAL.md`
- **Arquivos obrigatórios não vazios**
- **Template final sem placeholders** (erros): detecta `[Nome do Projeto]`, `____`, “preencher/insira/todo/tbd” etc. em `TEMPLATE_PROJETO_EDITAL.md`
- **Placeholders nas FASEs 1–4** (avisos): detecta `____`, `todo`, `tbd`

---

## Como as regras funcionam (EVL-like)

No relatório `FASE5_VALIDACAO.md`, cada achado deve ter:
- `rule_id`
- severidade (**erro** ou **aviso**)
- arquivo afetado
- evidência (trecho) quando aplicável
- fix sugerido

---

## Como adicionar/ajustar regras

Edite o workflow `workflows/validacao-projeto.yaml` para incluir novas regras (ou adicionar um checklist dedicado) e reexecute a Fase 5.

Dica: para evitar regras muito “frágeis”, prefira checks simples (existência, não-vazio, padrões grosseiros) no gate e deixe a análise qualitativa para a etapa de revisão QA.

---

## Integração no workflow

A Fase 5 já inclui instrução explícita de *gate* em:
- `workflows/validacao-projeto.yaml`

Ou seja: **sempre** rodar o gate EVL-like e **não** avançar se houver erros.
