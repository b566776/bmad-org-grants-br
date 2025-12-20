# Resumo: Adaptação do Método BMAD para Análise de Editais

## 📈 Visão Geral

O método **BMAD** (Build-Measure-Analyze-Decide), originalmente concebido para **Desenvolvimento Ágil Guiado por IA**, foi adaptado para criar um **framework estruturado de análise e elaboração de projetos para editais públicos**, fundações e organismos internacionais.

A adaptação transforma o ciclo iterativo de desenvolvimento de software em um **processo linear e progressivo** de construção de propostas, mantendo a filosofia de trabalho guiado por IA e iteração incremental.

---

## 🔄 Transformação: BMAD Original → BMAD Editais

### BMAD Original (Desenvolvimento de Software)

- **Build**: Construir incrementos de código
- **Measure**: Medir performance e qualidade
- **Analyze**: Analisar dados e feedback
- **Decide**: Decidir próximos passos

### BMAD Adaptado (Análise de Editais)

As 4 fases foram renomeadas e reinterpretadas para o contexto de elaboração de propostas:

#### **FASE 1 — ANALYSIS (Análise)**

**Equivalente ao "Measure + Analyze" original**

Compreender profundamente o edital e o contexto da organização proponente. A IA atua como **Analyst-PM** (Analista de Requisitos + Gerente de Projeto).

**Processo:**

1. Leitura automática do edital (conversão PDF → Markdown)
2. Incorporação da base de conhecimento da Organizaçãoexclusivamente do diretório `baseDeConhecimento/` e seus subdiretórios
3. Extração de requisitos críticos: objeto, público-alvo, valores, prazos, critérios de pontuação
4. Diagnóstico situacional: problemas, oportunidades, restrições

**Entrega:** `FASE1_ANALISE.md`
- Resumo executivo (≤2 parágrafos)
- Lista de até 12 perguntas estratégicas
- Quadro-resumo: Problema | Público | Oportunidades | Restrições | Pontos Fortes da ONG

#### **FASE 2 — PLANNING (Planejamento/Ideação)**

**Equivalente ao "Decide" original + Design Thinking**

Gerar ideias de projetos alinhadas ao edital. A IA atua como **Product Manager + Estratégista**.

**Processo:**

1. Brainstorming de 2-4 ideias de projetos
2. Para cada ideia: objetivo geral, objetivos específicos, público, resultados esperados, ODS
3. Análise comparativa de viabilidade (tabela de critérios)
4. Recomendação fundamentada

**Entrega:** `FASE2_PLANEJAMENTO.md`
- Ideias detalhadas com justificativas
- Tabela comparativa (Inovação | Impacto Social | Potencial de Mercado | Complexidade)
- Pergunta ao usuário: "Qual ideia deseja priorizar?"

---

#### **FASE 3 — SOLUTION (Solução/Desenho Técnico)**

**Equivalente ao "Build" original (arquitetura)**

Desenhar a proposta final escolhida. A IA atua como **Architect + Program Designer**.

**Processo:**

1. Título e resumo executivo
2. Justificativa com diagnóstico fundamentado
3. Objetivos (geral + 3-6 específicos mensuráveis)
4. Público-alvo detalhado com critérios de elegibilidade
5. Componentes/eixos de atuação
6. Matriz de indicadores (indicador | meta | fonte de verificação)
7. Estratégia de sustentabilidade
8. Alinhamento com ODS e metas específicas

**Entrega:** `FASE3_SOLUCAO.md`
- Proposta técnica completa e estruturada
- Pronta para ser transformada em documentos de submissão

---

#### **FASE 4 — IMPLEMENTATION (Implementação/Operacionalização)**

**Equivalente ao "Build" original (execução)**

Transformar a solução em plano operacional. A IA atua como **Scrum Master + Operations Manager**.

**Processo:**

1. Plano de trabalho detalhado (atividades, responsáveis, cronograma)
2. Estrutura orçamentária por blocos de despesa
3. Checklist de documentos exigidos pelo edital
4. Extração e confirmação de perguntas para submissão
5. Adaptação a formulários específicos (se fornecidos)
6. Cronograma de execução (diagrama de Gantt em Markdown)

**Entrega:** `FASE4_IMPLEMENTACAO.md`
- Plano de trabalho operacional
- Orçamento estruturado
- Perguntas de submissão respondidas
- Documentos de submissão prontos

---

#### **FASE 5 — VALIDATION (Validação Estrutural)**

**Novo conceito introduzido: Protocolo DAVID-ε · DVP**

Validar a coerência estrutural da proposta antes da submissão. A IA atua como **Validador de Coerência Estrutural**.

**Processo:**

1. Aplicação do protocolo DVP (David Validation Protocol)
2. Avaliação de 7 métricas estruturais ($m_1$ a $m_7$)
3. Cálculo da coerência estrutural global $C(S)$
4. Classificação: RESOLÚVEL | REFORMULÁVEL | ESTRUTURALMENTE INVIÁVEL
5. Geração de plano de ajustes (se necessário)

**Métricas Avaliadas:**
- $m_1$: Consistência interna (ausência de contradições)
- $m_2$: Alinhamento entre subsistemas (cronograma, orçamento, equipe)
- $m_3$: Estabilidade estrutural (robustez frente a riscos)
- $m_4$: Capacidade de emergência (potencial de impacto ampliado)
- $m_5$: Densidade informacional (qualidade das informações)
- $m_6$: Relação sinal/ruído (clareza da comunicação)
- $m_7$: Conservação de sentido global (alinhamento com edital e missão)

**Entrega:** `FASE5_VALIDACAO.md`
- Relatório completo de validação estrutural
- Pontuação detalhada de cada métrica
- Cálculo de $C(S)$ (coerência estrutural)
- Classificação e recomendações
- Parecer final de aprovação para submissão

---

## 🤖 Papel da IA em Cada Fase

| Fase | Papel da IA | Função Principal |
|------|-------------|------------------|
| **1 - Analysis** | Analyst-PM | Interpretar edital, diagnosticar contexto, extrair requisitos |
| **2 - Planning** | Product Manager | Gerar ideias, modelar propostas, recomendar estratégias |
| **3 - Solution** | Architect | Desenhar solução técnica completa e estruturada |
| **4 - Implementation** | Scrum Master | Operacionalizar plano, cronograma e orçamento |
| **5 - Validation** | Validador DVP | Aplicar protocolo de coerência estrutural DAVID-ε |

---

## 📚 Recursos e Links

- **README.md**: Visão geral do módulo BGb
- **IMPLEMENTATION_GUIDE.md**: Guia de implementação prática
- **docs/DAVID_DVP_PROTOCOL.md**: Protocolo de validação estrutural (Fase 5)
- **templates/TEMPLATE_PROJETO_EDITAL.md**: Template padrão para projetos
- **templates/TEMPLATE_VALIDACAO.md**: Template de relatório de validação DVP
- **agents/bmm-pm.customize.yaml**: Configuração da persona de PM
- **workflows/**: Workflows para cada fase (incluindo validacao-projeto.yaml)

---

**Desenvolvido por:** Usuário + Gemini AI  
**Contexto:** BGb – BMAD Grants Brazil (Foco: Amigos da Vida)  
**Data:** Dezembro 2025
