# bmad-org-grants-br

**Módulo BGb – BMAD Grants Brazil**

Módulo BMAD v6 para análise de editais e redação de projetos para organizações (foco: Organizações e Startups). Integração com install-custom e fluxo de uso.

## Resumo Executivo

**BGb (BMAD Grants Brazil)** é um framework estruturado que adapta o método BMAD (Build-Measure-Analyze-Decide) para análise de editais públicos, fundações e organismos internacionais. O método transforma o ciclo iterativo original em um processo linear e progressivo de construção de propostas, mantendo a filosofia de trabalho guiado por IA.

### ✨ Características Principais

- **4 Fases Estruturadas**: Analysis → Planning → Solution → Implementation
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

### Instalação A) Durante o Setup do BMAD (Recomendado)

Ao executar `npx bmad-method@alpha install`, responda:

1. **Will you be installing any official BMad modules?**
   → `No`

2. **Would you like to install a local custom module?**
   → `Yes`
   
3. **Path to your local custom module:**
   → `c:\Users\User\Documents\bmad-org-grants-br`

4. **Where should default output files be saved?**
   → `[ENTER]` para aceitar `_bmad-output`

**Pronto!** O módulo está instalado e os agentes foram configurados automaticamente durante o `install`.

---

### Instalação B) Após Setup do BMAD 
Se você já fez o `init` do BMAD e quer adicionar o módulo depois:

```bash
# Se o módulo está no GitHub
npx bmad-method@alpha install-custom \
  --from git \
  --repo https://github.com/b566776/bmad-org-grants-br.git

# OU se está local
npx bmad-method@alpha install-custom \
  --from local \
  --path c:\Users\User\Documents\bmad-org-grants-br
```

**Nota:** Na versão `@alpha`, não há comando `compile` separado. Os agentes são configurados automaticamente durante o `install` ou `install-custom`. Isso copia `agents/`, `workflows/`, `memories/` e `templates/` para `_bmad/modules/bmad-org-grants-br`.

---

## 📂 Configuração: Organizando Dados da Organização

Após a instalação, você precisa **preencher os diretórios** com as informações da sua organização.

### Passo 1: Localizar o Diretório da Organização

**Se instalou via Opção A (durante setup):**
```
_bmad/modules/bmad-org-grants-br/memories/organizations/default/
```

**Para criar organizações adicionais:**
```bash
python _bmad/modules/bmad-org-grants-br/scripts/create-organization.py \
  --name "Nome da Organização" \
  --type ngo
```

### Passo 2: Adicionar Documentos da Organização

Organize os documentos nas seguintes pastas:

#### 📄 `certidoes/` - Certidões e Registros Oficiais
```
certidoes/
├── cnpj.pdf                    # CNPJ da organização
├── certidao_federal.pdf        # Quitação de tributos federais
├── certidao_estadual.pdf       # Quitação de tributos estaduais
├── certidao_municipal.pdf      # Quitação de tributos municipais
├── certidao_fgts.pdf           # Regularidade FGTS
└── utilidade_publica.pdf       # Certificado de utilidade pública (se houver)
```

#### 💰 `documentos_bancarios/` - Dados Bancários
```
documentos_bancarios/
├── dados_bancarios.md          # Banco, agência, conta (em markdown)
└── comprovante_conta.pdf       # Comprovante de conta bancária
```

**Exemplo de `dados_bancarios.md`:**
```markdown
# Dados Bancários

**Banco:** Banco do Brasil
**Agência:** 1234-5
**Conta Corrente:** 67890-1
**CNPJ:** 12.345.678/0001-90
**Titular:** [Nome da Organização]
```

#### 🏛️ `documentos_institucionais/` - Governança e Demonstrativos
```
documentos_institucionais/
├── estatuto.pdf                # Estatuto social
├── ata_eleicao_diretoria.pdf   # Ata da última eleição
├── balanco_patrimonial.pdf     # Último balanço patrimonial
└── relatorio_atividades.pdf    # Relatório de atividades anual
```

#### 📊 `projetos_anteriores/` - Histórico de Projetos
```
projetos_anteriores/
├── projeto_2023_saude.md       # Projeto executado em 2023
├── projeto_2022_educacao.md    # Projeto executado em 2022
└── relatorios/
    ├── relatorio_final_2023.pdf
    └── certificado_conclusao_2023.pdf
```

**Exemplo de arquivo de projeto anterior:**
```markdown
# Projeto Saúde Comunitária 2023

**Financiador:** Fundação XYZ
**Valor:** R$ 150.000,00
**Período:** Jan/2023 - Dez/2023
**Status:** Concluído

## Resumo
Projeto de atenção básica à saúde...

## Resultados
- 500 atendimentos realizados
- 3 comunidades atendidas
```

### Passo 3: Preencher Metadados da Organização

Edite o arquivo `config.json`:

```json
{
  "organization_name": "ONG Exemplo de Direitos Humanos",
  "organization_type": "ngo",
  "cnpj": "12.345.678/0001-90",
  "areas_atuacao": ["direitos humanos", "assistência social", "educação"],
  "tags": ["ong", "terceiro-setor"],
  "color": "#2E7D32",
  "icon": "🤝"
}
```

**Tipos disponíveis:** `ngo`, `startup`, `company`, `institute`, `foundation`

### Passo 4: Executar Fase 1 para Gerar Portfolio

Após adicionar os documentos, execute a **Fase 1** do workflow:

```bash
# No agente BMAD PM, use:
INICIAR
```

O workflow irá:
1. ✅ Escanear todos os documentos nas subpastas
2. ✅ Extrair informações relevantes
3. ✅ **Gerar automaticamente** `ORGANIZATION_PORTFOLIO.md` consolidado
4. ✅ Criar `HISTORICO_EDITAIS.md` se não existir

**Resultado:** Portfolio completo gerado automaticamente! 🎉

### Passo 5: Verificar Portfolio Gerado

Confira o arquivo gerado:
```
_bmad/modules/bmad-org-grants-br/memories/organizations/default/ORGANIZATION_PORTFOLIO.md
```

Edite manualmente se necessário para complementar informações.

---

## 🔄 Gerenciamento Multi-Organizações

### Listar Organizações Disponíveis

**⚠️ Importante:** O comando acima NÃO copia os scripts Python e configs automaticamente.

#### Opção A: Instalação Automatizada (Recomendado)

**Linux/Mac:**
```bash
cd _bmad/modules/bmad-org-grants-br
curl -O https://raw.githubusercontent.com/SUA_ORG/bmad-org-grants-br/main/install.sh
chmod +x install.sh
./install.sh
```

**Windows (PowerShell como Administrador):**
```powershell
cd _bmad/modules/bmad-org-grants-br
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/SUA_ORG/bmad-org-grants-br/main/install.ps1" -OutFile "install.ps1"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1
```

O script irá:
- ✅ Clonar o repositório temporariamente
- ✅ Copiar scripts Python e configurações
- ✅ Instalar dependências (opcional)
- ✅ Limpar arquivos temporários

#### Opção B: Instalação Manual

Clone o repositório e copie manualmente:

```bash
# Clone do repositório
git clone https://github.com/SUA_ORG/bmad-org-grants-br.git temp-bgb

# Navegue até o diretório do módulo instalado
cd _bmad/modules/bmad-org-grants-br

# Copie os scripts Python
cp ../../../temp-bgb/pdf_converter.py .
cp ../../../temp-bgb/converter_pdf_md.py .
cp ../../../temp-bgb/converter_pdfs_batch.py .
cp ../../../temp-bgb/requirements.txt .

# Copie a pasta config
cp -r ../../../temp-bgb/config .

# Copie a pasta docs (opcional, para referência local)
cp -r ../../../temp-bgb/docs .

# Limpe o diretório temporário
cd ../../..
rm -rf temp-bgb
```

**Alternativa Windows (PowerShell):**
```powershell
# Clone do repositório
git clone https://github.com/SUA_ORG/bmad-org-grants-br.git temp-bgb

# Navegue até o diretório do módulo instalado
cd _bmad/modules/bmad-org-grants-br

# Copie os scripts Python
Copy-Item ..\..\..\temp-bgb\pdf_converter.py .
Copy-Item ..\..\..\temp-bgb\converter_pdf_md.py .
Copy-Item ..\..\..\temp-bgb\converter_pdfs_batch.py .
Copy-Item ..\..\..\temp-bgb\requirements.txt .

# Copie as pastas
Copy-Item ..\..\..\temp-bgb\config -Recurse .
Copy-Item ..\..\..\temp-bgb\docs -Recurse .

# Limpe o diretório temporário
cd ..\..\..
Remove-Item temp-bgb -Recurse -Force
```

### Passo 3: Instalar Dependências Python

```bash
cd _bmad/modules/bmad-org-grants-br
pip install -r requirements.txt
```

### Passo 4: Compilar Agentes BMAD

```bash
npx bmad-method@alpha install
```

Escolher compilar todos os agentes para aplicar a customização (`bmm-pm.customize.yaml`).

### Dependências Python (Conversão de PDFs)

Para usar os scripts de conversão de PDF para Markdown:

```bash
pip install -r requirements.txt
```

Isso instalará:
- **Docling** (primário) - Engine avançado com OCR, tabelas e fórmulas
- **pypdf** (fallback) - Engine básico para PDFs simples

---

## 🔄 Conversão de PDFs 

O módulo inclui scripts para converter PDFs de editais e documentos para Markdown automaticamente:

### Converter um único PDF:
```bash
python converter_pdf_md.py "memories/editais/edital.pdf"
```

### Converter todos os PDFs em lote:
```bash
python converter_pdfs_batch.py "memories" --recursive
```

**Veja mais:** [CONVERSAO_PDF.md](./docs/CONVERSAO_PDF.md) para documentação completa.

---

## 📋 Fluxo de Uso Diário

### Para um novo edital:

1. **Criar arquivo do edital**: `memories/editais/[edital-nome].md` com resumo extraído do PDF
2. **Fase 1 - Análise**: Usar comando `INICIAR` no agente → gera `FASE1_ANALISE.md` + **captura perguntas do formulário** (manual ou via `EXTRAIR QUESTIONARIO`)
3. **Fase 2 - Planejamento**: Usar `IR PARA FASE 2` → gera `FASE2_PLANEJAMENTO.md` com ideias de projetos + **inicia redação estratégica do `QUESTIONARIO_PREENCHIDO.md`** (respostas completas, coesas, sem redundância)
4. **Fase 3 - Solução**: Usar `IR PARA FASE 3` → preenche `TEMPLATE_PROJETO_EDITAL.md` e gera `FASE3_SOLUCAO.md` (mantendo `QUESTIONARIO_PREENCHIDO.md` em sincronia)
5. **Fase 4 - Implementação**: Usar `IR PARA FASE 4` → gera `FASE4_IMPLEMENTACAO.md` com plano de trabalho, orçamento e checklist (finaliza `QUESTIONARIO_PREENCHIDO.md`)
6. **(Opcional) Preencher Formulário via Browser**: Usar `PREENCHER FORMULARIO` → cola respostas no formulário web (sem enviar)

### Comandos de Navegação

O usuário controla o fluxo através de comandos explícitos:

- `INICIAR` → Inicia Fase 1 (inclui análise do edital)
- `EXTRAIR QUESTIONARIO` → Captura perguntas do formulário via browser (Fase 1)
- `IR PARA FASE 2` → Avança para Fase 2 (gera ideias + inicia redação de respostas)
- `IR PARA FASE 3` → Avança para Fase 3 (desenho técnico completo)
- `IR PARA FASE 4` → Avança para Fase 4 (operacionalização + orçamento)
- `PREENCHER FORMULARIO` → Preenche formulário web via browser (sem enviar)
- `REFAZER FASE X` → Refaz uma fase específica

---

## 🎁 Features Opcionais

### Sistema de Links Úteis Categorizados

Arquivo JSON com +50 links organizados em 8 categorias:
- Editais federais (SICONV, CNPq)
- Fundações e institutos
- Dados e indicadores (IBGE, IPEA, ODS)
- Legislação e normas
- Capacitação e ferramentas

**Localização:** [`memories/links_uteis.json`](./memories/links_uteis.json)

### Análise Preditiva de Chances de Aprovação

Script Python que estima probabilidade de aprovação baseado em 7 critérios:
- Alinhamento com Edital (20%)
- Adequação Orçamentária (15%)
- Qualificação da Equipe (15%)
- Inovação, Impacto Social, Sustentabilidade (30%)

**Uso:**
```bash
python approval_predictor.py memories/editais/edital-xyz/projeto/
```

**Documentação completa:** [FEATURES_OPCIONAIS.md](./docs/FEATURES_OPCIONAIS.md)

---

## 🏢 Suporte Multi-Organizações (Multi-Tenant)

**Novidade:** O módulo agora suporta **múltiplas organizações** em uma única instalação!

### Casos de Uso

- **Consultores:** Atender múltiplos clientes sem reinstalar
- **ONGs compartilhadas:** Diferentes setores da mesma org
- **Portabilidade:** Backup/restore por organização

### Gerenciamento de Perfis

```bash
# Listar todas as organizações
python scripts/list-organizations.py

# Trocar organização ativa
python scripts/switch-organization.py nome-da-organizacao

# Criar nova organização
python scripts/create-organization.py --name "Nova ONG" --type ngo

# Tutorial completo em: memories/organizations/README.md
```

### Estrutura

```
memories/organizations/
├── .current                      # Perfil ativo
├── default/                      # Perfil padrão
│   ├── config.json               # Metadados da org
│   ├── ORGANIZATION_PORTFOLIO.md
│   └── ...
└── outra-organizacao/            # Outro perfil
    └── ...
```

**Isolamento total:** Cada organização tem seus próprios documentos, editais e histórico.

---

## 📂 Como Funciona a Memória Organizacional

O módulo usa uma arquitetura **híbrida de duas camadas**:

### 1. **Fonte Primária** (Subpastas em `memories/`)
Documentos originais organizados por categoria:
- `certidoes/` - Certidões e registros oficiais
- `documentos_bancarios/` - Dados bancários
- `documentos_institucionais/` - Estatuto, atas, balanços
- `projetos_anteriores/` - Histórico detalhado de projetos

### 2. **Sumário Executivo** (`ORGANIZATION_PORTFOLIO.md`)
Arquivo **gerado automaticamente** que consolida informações das subpastas:
- Criado na primeira execução da Fase 1
- Atualizado quando conteúdo de `memories/` muda
- Otimizado para uso eficiente pelos workflows (contexto LLM)

**Vantagens desta Arquitetura:**
- ✅ Performance: Processar 1 arquivo consolidado vs. 50+ arquivos/fase
- ✅ Contexto: Informações estruturadas e priorizadas para redação
- ✅ Manutenção: Adicione arquivos em subpastas → portfolio se atualiza
- ✅ Flexibilidade: Organize documentos como preferir

---

## 📁 Estrutura do Repositório

```
bmad-org-grants-br/
├── pdf_converter.py                   # Módulo de conversão PDF
├── converter_pdf_md.py                # Script conversão individual
├── converter_pdfs_batch.py            # Script conversão em lote
├── approval_predictor.py              # Análise preditiva de aprovação
├── requirements.txt                   # Dependências Python
├── install.sh / install.ps1           # Scripts de instalação
├── config/
│   └── config.json                    # Configuração de PDF
├── agents/
│   └── bmm-pm.customize.yaml          # Agente PM
├── memories/
│   ├── ORGANIZATION_PORTFOLIO.md      # Sumário executivo (auto-gerado)
│   ├── HISTORICO_EDITAIS.md           # Rastreamento de editais
│   ├── links_uteis.json               # Links categorizados
│   ├── certidoes/                     # Certidões e registros
│   ├── documentos_bancarios/          # Dados bancários
│   ├── documentos_institucionais/     # Estatuto, atas, balanços
│   ├── projetos_anteriores/           # Histórico de projetos  
│   └── logs/                          # Logs de conversão
├── templates/
│   ├── TEMPLATE_PROJETO_EDITAL.md     # Template de proposta
├── workflows/
│   ├── analise-edital.yaml            # FASE 1
│   ├── ideias-projeto.yaml            # FASE 2
│   ├── desenho-projeto.yaml           # FASE 3
│   ├── questionario-submissao.yaml    # Checkpoint pós-FASE 2
│   ├── implementacao-projeto.yaml     # FASE 4
│   ├── arquivar-projeto.yaml          # Arquivamento
│   └── review-proposal.yaml           # Revisão QA
├── docs/
│   ├── BMAD_EDITAIS_OVERVIEW.md       # Visão geral
│   ├── CONVERSAO_PDF.md               # Conversão PDF
│   └── FEATURES_OPCIONAIS.md          # Features extras
├── IMPLEMENTATION_GUIDE.md
├── README.md (este arquivo)
└── module.yaml
```

---

## 🔄 4 Fases do BMAD-Editais

| Fase | Nome | Objetivo | Saída |
|------|------|----------|-------|
| **1** | **ANALYSIS** | Compreender edital e contexto | `FASE1_ANALISE.md` |
| **2** | **PLANNING** | Gerar ideias de projetos alinhadas | `FASE2_PLANEJAMENTO.md` |
| **3** | **SOLUTION** | Desenhar proposta técnica completa | `FASE3_SOLUCAO.md` |
| **4** | **IMPLEMENTATION** | Operacionalizar plano e orçamento | `FASE4_IMPLEMENTACAO.md` |

Cada fase possui um agente IA especializado que atua com um papel distinto:

- **Fase 1**: Analyst-PM (Analista de Requisitos + Gerente de Projeto)
- **Fase 2**: Product Manager + Estrategista
- **Fase 3**: Architect + Program Designer
- **Fase 4**: Scrum Master + Operations Manager

---

## 📚 Recursos

### Documentação Principal
- Visão geral: [docs/BMAD_EDITAIS_OVERVIEW.md](./docs/BMAD_EDITAIS_OVERVIEW.md)
- Guia de implementação: [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)
- Conversão PDF: [docs/CONVERSAO_PDF.md](./docs/CONVERSAO_PDF.md)

### Features Opcionais
- **Documentação**: [docs/FEATURES_OPCIONAIS.md](./docs/FEATURES_OPCIONAIS.md)
- **Links úteis**: [memories/links_uteis.json](./memories/links_uteis.json)
- **Análise preditiva**: `approval_predictor.py`

### Templates
- Proposta: [templates/TEMPLATE_PROJETO_EDITAL.md](./templates/TEMPLATE_PROJETO_EDITAL.md)

---

**Desenvolvido por:** Usuário + Gemini AI  
**Contexto:** BGb – BMAD Grants Brazil (Foco: Organização)  
**Data:** Dezembro 2025
