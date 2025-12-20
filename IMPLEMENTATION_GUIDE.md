# Guia de Implementação - Módulo BGb: Análise de Editais e Redação de Projetos

## Visão Geral

Este módulo estende o BMAD v6 para criar um sistema especializado de análise de editais e redação de projetos. Está configurado especialmente para a organização **Amigos da Vida**, mas pode ser adaptado para qualquer ONG.

## Estrutura de Diretórios

```
bmad-org-grants-br/
├─ module.yaml                        # Configuração principal do módulo
├─ README.md                           # Documentação do módulo
├─ IMPLEMENTATION_GUIDE.md             # Este arquivo
├─ agents/
│  └─ bgb-pm.customize.yaml           # Agente PM customizado para editais
├─ workflows/
│  ├─ analise-edital.yaml            # Workflow para análise de editais
│  └─ ideias-projeto.yaml            # Workflow para geração de ideias
├─ memories/
│  ├─ ONG_PORTFOLIO.md                # Portfólio estático da ONG
│  └─ exemplos-editais/
│     └─ edital-exemplo-1.md          # Exemplo de edital processado
└─ templates/
   └─ TEMPLATE_PROJETO_EDITAL.md      # Template para redacao de projetos
```

## Próximos Passos de Implementação

### 1. Criar Agente Customizado (agents/bgb-pm.customize.yaml)

O agente PM será configurado como especialista em editais:
- Persona: Especialista em elaboração de projetos sociais
- Menu customizado com opcoes: analisar-edital, ideias-projeto, projeto-completo
- Memórias sobre a ONG Amigos da Vida
- Prompts reutilizáveis para ações específicas

### 2. Criar Workflows (workflows/)

- **analise-edital.yaml**: Lê o PDF do edital, gera resumo técnico, checklist de requisitos
- **ideias-projeto.yaml**: Propoe 3-4 ideias de projeto alinhadas ao edital

### 3. Criar Memórias (memories/)

- **ONG_PORTFOLIO.md**: Histórico, açoes, resultados, dados da Amigos da Vida
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
   - Crie/adicione `memories/editais/<nome-edital>.md`
   - Carregue o PDF e extraia os pontos-chave

2. **Análise**:
   - No IDE, abra um agente BMAD
   - Acione o menu `*analisar-edital`
   - Revise resumo, checklist e recomendações

3. **Ideias**:
   - Acione `*ideias-projeto`
   - Selecione a ideia mais promissora

4. **Redação**:
   - Acione `*projeto-completo`
   - Revise e adapte o rascunho do projeto
   - Finalize para submissão

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

### Documentação das Fases

Para descrição detalhada de cada fase, objetivos, entregas e papéis de IA, consulte:

- [docs/BMAD_EDITAIS_OVERVIEW.md](./docs/BMAD_EDITAIS_OVERVIEW.md)

---
- [BMAD Sample Modules](https://github.com/b566776/BMAD-METHOD/tree/main/docs/sample-custom-modules)
