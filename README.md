# bmad-org-grants-br

**Módulo BGb – BMAD Grants Brazil**

Módulo BMAD v6 para análise de editais e redação de projetos para organizações (foco: Organizações e Startups). Integração com install-custom e fluxo de uso.

## Resumo Executivo

**BGb (BMAD Grants Brazil)** é um framework estruturado que adapta o método BMAD (Build-Measure-Analyze-Decide) para análise de editais públicos, fundações e organismos internacionais. O método transforma o ciclo iterativo original em um processo linear e progressivo de construção de propostas, mantendo a filosofia de trabalho guiado por IA.

### ✨ Características Principais

- 5 Fases Estruturadas**: Analysis → Planning → Solution → Implementation  → Validation
- **IA Especializada em Cada Fase**: Analista, Estrategista, Arquiteto, Gestor
- **Base de Conhecimento Integrada**: Memória automática da organização (portfólio, relatórios, certificações)
- **Templates Prontos**: Estrutura padronizada para todas as propostas
- **Rastreabilidade Completa**: Histórico de editais e versões de projetos

---

## 📖 Documentação

- **[BMAD_EDITAIS_OVERVIEW.md](./docs/BMAD_EDITAIS_OVERVIEW.md)**: Documentação completa do método BMAD adaptado para editais
- **[IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)**: Guia de implementação e uso prático
- **[module.yaml](./module.yaml)**: Configuração do módulo

---

## 🚀 Instalação

Crie o repositório https://github.com/SUA_ORG/bmad-org-grants-br.git com a estrutura acima.

Dentro de um projeto BMAD já instalado, rodar:

```bash
npx bmad-method@alpha install-custom \
  --from git \
  --repo https://github.com/SUA_ORG/bmad-org-grants-br.git
```

Isso copia `agents/`, `workflows/`, `memories/` e `templates/` para `_bmad/modules/bmad-org-grants-br`.

### Configuração Final

```bash
npx bmad-method@alpha install
```

Escolher compilar todos os agentes para aplicar a customização (`bmm-pm.customize.yaml`).

---

## 📋 Fluxo de Uso Diário

### Para um novo edital:

1. **Criar arquivo do edital**: `memories/editais/[edital-nome].md` com resumo extraído do PDF
2. **Fase 1 - Análise**: Usar comando `INICIAR` no agente → gera `FASE1_ANALISE.md`
3. **Fase 2 - Planejamento**: Usar `IR PARA FASE 2` → gera `FASE2_PLANEJAMENTO.md` com ideias de projetos
4. **Fase 3 - Solução**: Usar `IR PARA FASE 3` → preenche `TEMPLATE_PROJETO_EDITAL.md` e gera `FASE3_SOLUCAO.md`
5. **Fase 4 - Implementação**: Usar `IR PARA FASE 4` → gera `FASE4_IMPLEMENTACAO.md` com plano de trabalho, orçamento e checklist
6. 6. **Fase 5 - Validação**: Usar `VALIDAR` → gera `FASE5_VALIDACAO.md` com verificação de coeência estrutural (DVP-DAVID)

### Comandos de Navegação

O usuário controla o fluxo através de comandos explícitos:

- `INICIAR` → Inicia Fase 1
- `IR PARA FASE 2` → Avança para Fase 2
- `IR PARA FASE 3` → Avança para Fase 3
- `IR PARA FASE 4` → Avança para Fase 4
- `REFAZER FASE X` → Refaz uma fase específica

---

- `IR PARA FASE 5` → Avança para Fase 5
## 📁 Estrutura do Repositório

```
bmad-org-grants-br/
├── agents/
│   └── bmm-pm.customize.yaml          # Persona de PM com 4 fases
├── memories/
│   ├── ORGANIZATION_PORTFOLIO.md      # Portfólio da organização
│   └── editais/                       # Editais processados
├── memória estática /exemplos-editais/  # Exemplos de editais para referência
├── templates/
│   └── TEMPLATE_PROJETO_EDITAL.md     # Template de proposta
├── workflows/
│   ├── analise-edital.yaml            # FASE 1
│   ├── ideias-projeto.yaml            # FASE 2
│   ├── desenho-projeto.yaml           # FASE 3
│   └── implementacao-projeto.yaml     # FASE 4
├── docs/
│   └── BMAD_EDITAIS_OVERVIEW.md       # Documentação completa
├── IMPLEMENTATION_GUIDE.md
├── README.md (este arquivo)
└── module.yaml
```

---

## 🔄5  Fases do BMAD-Editais

| Fase | Nome | Objetivo | Saída |
|------|------|----------|-------|
| **1** | **ANALYSIS** | Compreender edital e contexto | `FASE1_ANALISE.md` |
| **2** | **PLANNING** | Gerar ideias de projetos alinhadas | `FASE2_PLANEJAMENTO.md` |
| **3** | **SOLUTION** | Desenhar proposta técnica completa | `FASE3_SOLUCAO.md` |
| **4** | **IMPLEMENTATION** | Operacionalizar plano e orçamento | `FASE4_IMPLEMENTACAO.md`
| **5** | **VALIDATION** | Validar coerência estrutural da proposta | `FASE5_VALIDACAO.md` ||

Cada fase possui um agente IA especializado que atua com um papel distinto:

- **Fase 1**: Analyst-PM (Analista de Requisitos + Gerente de Projeto)
- **Fase 2**: Product Manager + Estrategista
- **Fase 3**: Architect + Program Designer
- **Fase 4**: Scrum Master + Operations Manager
- - **Fase 5**: Validador de Coeência Estrutural (DVP-DAVID)

---

## 📚 Recursos

- Documentação detalhada: [docs/BMAD_EDITAIS_OVERVIEW.md](./docs/BMAD_EDITAIS_OVERVIEW.md)
- Guia de implementação: [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)
- Template de proposta: [templates/TEMPLATE_PROJETO_EDITAL.md](./templates/TEMPLATE_PROJETO_EDITAL.md)

---

**Desenvolvido por:** Usuário + Gemini AI  
**Contexto:** BGb – BMAD Grants Brazil (Foco: Amigos da Vida)  
**Data:** Dezembro 2025
