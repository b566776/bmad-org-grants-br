# Guia de Implementação - Módulo BGb: Análise de Editais e Redação de Projetos

## Visão Geral

Este módulo estende o BMAD v6 para criar um sistema especializado de análise de editais e redação de projetos. Está configurado especialmente para a organização **Organização**, mas pode ser adaptado para qualquer ONG.

## Estrutura de Diretórios

```
bmad-org-grants-br/
├─ module.yaml                        # Configuração principal do módulo
├─ README.md                           # Documentação do módulo
├─ IMPLEMENTATION_GUIDE.md             # Este arquivo
├─ requirements.txt                    # Dependências Python (Docling, pypdf)
├─ pdf_converter.py                    # Módulo de conversão PDF
├─ converter_pdf_md.py                 # Script conversão individual
├─ converter_pdfs_batch.py             # Script conversão em lote
├─ config/
│  └─ config.json                      # Configurações de conversão PDF
├─ docs/
│  ├─ BMAD_EDITAIS_OVERVIEW.md         # Visão geral do método
│  └─ CONVERSAO_PDF.md                 # Documentação de conversão PDF
├─ agents/
│  └─ bmm-pm.customize.yaml            # Agente PM customizado
├─ workflows/
│  ├─ analise-edital.yaml              # Fase 1 - Análise
│  ├─ ideias-projeto.yaml              # Fase 2 - Planejamento
│  ├─ questionario-submissao.yaml      # Checkpoint pós-Fase 2 (formulário)
│  ├─ implementacao-projeto.yaml       # Fase 4 - Implementação
│  ├─ arquivar-projeto.yaml            # Arquivamento de projetos
│  └─ review-proposal.yaml             # Revisão de qualidade
├─ memories/
│  ├─ ORGANIZATION_PORTFOLIO.md        # Portfólio da organização
│  ├─ editais/                         # Editais processados
│  ├─ editais-anteriores/              # Histórico de editais
│  └─ logs/
│     └─ conversao_pdfs_log.txt        # Log de conversões PDF
└─ templates/
   ├─ TEMPLATE_PROJETO_EDITAL.md       # Template de proposta
 
```

## Configuração Inicial

### Instalação de Dependências Python

Antes de usar o módulo, instale as dependências para conversão de PDFs:

```bash
cd bmad-org-grants-br
pip install -r requirements.txt
```

Isso instalará:
- **Docling** (primário): Engine avançado com OCR, tabelas e fórmulas
- **pypdf** (fallback): Engine básico para PDFs simples

### Estrutura de Memórias Recomendada

Organize a memória da organização em `memories/` (no repositório) e `.bmad-custom/memories/` (após instalação):

```
_bmad/modules/bmad-org-grants-br/memories/  # Memórias estáticas do módulo
├── ORGANIZATION_PORTFOLIO.md                # Portfólio principal (Markdown)
└── logs/
    └── conversao_pdfs_log.txt               # Log automático de conversões

.bmad-custom/memories/                       # Conteúdo dinâmico do usuário
├── editais/                                 # Editais em processamento
│   └── [edital-nome]/
│       ├── edital.pdf
│       ├── edital.md                        # Gerado automaticamente
│       └── projeto/
│           ├── FASE1_ANALISE.md
│           ├── FASE2_PLANEJAMENTO.md
│           ├── FASE3_SOLUCAO.md
│           └── FASE4_IMPLEMENTACAO.md
│
└── editais-anteriores/                      # Histórico de projetos concluídos
    └── [edital-nome-anterior]/
        ├── edital.pdf
        └── projeto/
```

## Próximos Passos de Implementação

### 1. Criar Agente Customizado (agents/bgb-pm.customize.yaml)

O agente PM será configurado como especialista em editais:
- Persona: Especialista em elaboração de projetos sociais
- Menu customizado com opcoes: analisar-edital, ideias-projeto, projeto-completo
- Memórias sobre a Organização
- Prompts reutilizáveis para ações específicas

### 2. Criar Workflows (workflows/)

- **analise-edital.yaml**: Lê o PDF do edital, gera resumo técnico, checklist de requisitos
- **ideias-projeto.yaml**: Propoe 3-4 ideias de projeto alinhadas ao edital

### 3. Criar Memórias (memories/)

- **ONG_PORTFOLIO.md**: Histórico, açoes, resultados, dados da Organização
- **exemplos-editais/**: Editais já processados para referência

### 4. Criar Template (templates/)

- **TEMPLATE_PROJETO_EDITAL.md**: Estrutura padrão para projetos (problema, objetivos, atividades, etc.)

## Instalação do Módulo

Depois que todos os arquivos forem criados, instale o módulo no seu projeto BMAD v6:

```bash
npx bmad-method@alpha install-custom \
  --from git \
  --repo https://github.com/seu-usuario/bmad-org-grants-br.git
```

Então, compile os agentes:

```bash
npx bmad-method@alpha install
# Escolha: "Compile all agents"
```

## Fluxo de Uso

### Dia a dia:

1. **Novo Edital**:
   - Crie/adicione `.bmad-custom/memories/editais/<nome-edital>.md`
   - Carregue o PDF e extraia os pontos-chave

2. **Análise**:
   - No IDE, abra um agente BMAD
   - Acione o menu `*analisar-edital`
   - Revise resumo, checklist e recomendações

3. **Ideias**:
   - Acione `*ideias-projeto`
   - Selecione a ideia mais promissora

4. **Questionário de Submissão (checkpoint)**:
   - Acione `*questionario-submissao`
   - Cole o rol de perguntas e limites (ou forneça a URL do formulário)
   - Gere `QUESTIONARIO_PREENCHIDO.md` pronto para copiar/colar

5. **Redação (Fase 3)**:
   - Acione `*projeto-completo`
   - Revise e adapte o rascunho do projeto
   - Garanta que `QUESTIONARIO_PREENCHIDO.md` esteja coerente e dentro dos limites

6. **Implementação (Fase 4)**:
   - Acione `*implementacao-projeto`
   - Gere `FASE4_IMPLEMENTACAO.md` e valide consistência meta↔orçamento
   - Garanta que `QUESTIONARIO_PREENCHIDO.md` continue coerente e dentro dos limites

## Referências

- [BMAD v6 - Agent Customization Guide](https://github.com/b566776/BMAD-METHOD/blob/main/docs/agent-customization-guide.md)
- [BMAD v6 - Custom Content Installation](https://github.com/b566776/BMAD-METHOD/blob/main/docs/custom-content-installation.md)
- 
## Mapeamento: Fases BMAD → Workflows → Entregáveis

O módulo implementa as 4 fases do BMAD adaptado para editais. Cada fase possui um workflow dedicado que gera documentos estruturados:

| Fase | Workflow | Saída |
|------|----------|-------|
| **1 - ANALYSIS** | `analise-edital.yaml` | `FASE1_ANALISE.md` |
| **2 - PLANNING** | `ideias-projeto.yaml` | `FASE2_PLANEJAMENTO.md` |
| **3 - SOLUTION** | `desenho-projeto.yaml` | `FASE3_SOLUCAO.md` + `TEMPLATE_PROJETO_EDITAL.md` (preenchido) |
| **4 - IMPLEMENTATION** | `implementacao-projeto.yaml` | `FASE4_IMPLEMENTACAO.md` |

Checkpoint recomendado (pós-Fase 2):
- `questionario-submissao.yaml` → `QUESTIONARIO_PREENCHIDO.md`

### Documentação das Fases

Para descrição detalhada de cada fase, objetivos, entregas e papéis de IA, consulte:

- [docs/BMAD_EDITAIS_OVERVIEW.md](./docs/BMAD_EDITAIS_OVERVIEW.md)

---
- [BMAD Sample Modules](https://github.com/b566776/BMAD-METHOD/tree/main/docs/sample-custom-modules)
