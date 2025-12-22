# Conversão de PDF para Markdown

Este documento explica como funciona a conversão de PDFs para Markdown no módulo **bmad-org-grants-br**, incluindo as diferenças entre os engines disponíveis e como configurá-los.

---

## Visão Geral

O módulo utiliza dois engines para conversão de PDFs:

1. **Docling** (primário) - Engine avançado com compreensão de layout, tabelas, fórmulas e OCR
2. **pypdf** (fallback) - Engine básico para extração simples de texto

O sistema detecta automaticamente qual engine está disponível e faz fallback automático se necessário.

---

## Engines Disponíveis

### Docling

**Vantagens:**
- Compreensão avançada de layout PDF
- Preservação completa de estrutura de tabelas
- Suporte a fórmulas matemáticas e código
- OCR integrado para PDFs escaneados
- Melhor ordenação de leitura baseada no layout
- Exportação Markdown de alta qualidade
- Suporte a múltiplos formatos (PDF, DOCX, PPTX, XLSX, etc.)

**Desvantagens:**
- Pode ser mais lento para PDFs simples
- Requer mais recursos (modelos ML)
- Primeira instalação pode demorar (download de modelos)

**Instalação:**
```bash
pip install docling
```

### pypdf

**Vantagens:**
- Leve e rápido
- Instalação simples
- Adequado para PDFs simples com texto puro

**Desvantagens:**
- Não preserva estrutura de tabelas
- Não mantém ordenação de leitura correta
- Não extrai fórmulas ou código adequadamente
- Não suporta OCR para PDFs escaneados
- Layout complexo é perdido

**Instalação:**
```bash
pip install pypdf
```

---

## Scripts Disponíveis

### converter_pdf_md.py

Converte um único PDF para Markdown.

**Uso básico:**
```bash
python converter_pdf_md.py "memories/editais/edital.pdf"
```

**Opções:**
```bash
python converter_pdf_md.py "documento.pdf" --engine docling
python converter_pdf_md.py "documento.pdf" --engine pypdf
python converter_pdf_md.py "documento.pdf" --engine auto --verbose
```

**Parâmetros:**
- `pdf_path` - Caminho para o arquivo PDF (obrigatório)
- `output_path` - Caminho de saída (opcional, usa mesmo diretório do PDF)
- `--engine` - Engine a usar: `docling`, `pypdf`, ou `auto` (padrão: `auto`)
- `--verbose` / `-v` - Mostra informações detalhadas

### converter_pdfs_batch.py

Converte múltiplos PDFs em lote, mantendo log de conversões.

**Uso básico:**
```bash
python converter_pdfs_batch.py "memories"
```

**Opções:**
```bash
python converter_pdfs_batch.py "memories" --recursive
python converter_pdfs_batch.py "memories/editais" --engine docling --verbose
```

**Parâmetros:**
- `directory` - Diretório a processar (obrigatório)
- `--recursive` / `-r` - Processa subdiretórios recursivamente
- `--engine` - Engine a usar: `docling`, `pypdf`, ou `auto` (padrão: `auto`)
- `--verbose` / `-v` - Mostra informações detalhadas

**Características:**
- Mantém log em `memories/logs/conversao_pdfs_log.txt`
- Evita reprocessar PDFs já convertidos
- Reconverte apenas se o PDF foi modificado após a conversão
- Mostra estatísticas de conversão por engine

---

## Configuração

As configurações de conversão estão em `config/config.json`:

```json
{
  "pdf_conversion": {
    "default_engine": "auto",
    "fallback_to_pypdf": true,
    "docling_options": {
      "enable_ocr": true,
      "preserve_tables": true,
      "preserve_formulas": true
    }
  }
}
```

### Opções de Configuração

- **default_engine**: Engine padrão a usar
  - `"auto"` - Detecta automaticamente (prioriza Docling se disponível)
  - `"docling"` - Força uso do Docling
  - `"pypdf"` - Força uso do pypdf

- **fallback_to_pypdf**: Se `true`, tenta fallback automático para pypdf se Docling falhar

- **docling_options**: Opções específicas do Docling
  - `enable_ocr`: Habilita OCR para PDFs escaneados
  - `preserve_tables`: Preserva estrutura de tabelas
  - `preserve_formulas`: Preserva fórmulas matemáticas

---

## Como Funciona o Fallback

O sistema funciona da seguinte forma:

1. **Detecção**: Verifica qual engine está disponível
2. **Tentativa**: Tenta usar o engine escolhido (ou detectado automaticamente)
3. **Fallback**: Se falhar e `fallback_to_pypdf` estiver habilitado, tenta pypdf
4. **Erro**: Se ambos falharem, retorna erro descritivo

**Exemplo de fluxo:**
```
1. Engine escolhido: docling
2. Docling disponível? Sim
3. Tenta converter com Docling
4. Sucesso? Sim → Retorna resultado
   Não → Fallback habilitado? Sim → Tenta pypdf
```

---

## Qual Engine Usar?

### Use Docling quando:
- PDF tem tabelas complexas
- PDF tem fórmulas matemáticas
- PDF tem layout complexo (colunas, cabeçalhos, rodapés)
- PDF é escaneado (requer OCR)
- Precisa de máxima qualidade na conversão

### Use pypdf quando:
- PDF é simples (texto puro)
- Precisa de velocidade máxima
- Docling não está disponível
- Recursos computacionais são limitados

### Use auto quando:
- Quer que o sistema escolha automaticamente
- Não tem preferência específica
- Quer fallback automático

---

## Troubleshooting

### Erro: "Docling não está disponível"

**Solução:**
```bash
pip install docling
```

Se a instalação falhar, o sistema usará pypdf automaticamente como fallback.

### Erro: "Nenhum engine de conversão disponível"

**Solução:**
Instale pelo menos um dos engines:
```bash
pip install -r requirements.txt
# OU individualmente:
pip install docling
pip install pypdf
```

### Conversão muito lenta

**Possíveis causas:**
- Docling está processando PDFs complexos (normal)
- Primeira execução (download de modelos)
- PDF muito grande

**Soluções:**
- Use `--engine pypdf` para PDFs simples
- Aguarde a primeira execução (download de modelos)
- Considere processar PDFs menores

### Tabelas não estão sendo preservadas

**Causa:** Provavelmente está usando pypdf

**Solução:**
```bash
python converter_pdf_md.py "documento.pdf" --engine docling
```

### PDF escaneado não está sendo convertido

**Causa:** pypdf não suporta OCR

**Solução:**
```bash
# Instale Docling
pip install docling

# Use Docling explicitamente
python converter_pdf_md.py "documento.pdf" --engine docling
```

---

## Log de Conversões

O script `converter_pdfs_batch.py` mantém um log em:
```
memories/logs/conversao_pdfs_log.txt
```

**Formato:**
```
PDF_PATH | MD_PATH | TIMESTAMP | ENGINE
```

O log é usado para:
- Evitar reprocessar PDFs já convertidos
- Rastrear qual engine foi usado em cada conversão
- Identificar quando reconverter é necessário (PDF modificado)

---

## Exemplos de Uso

### Converter um edital
```bash
python converter_pdf_md.py "memories/editais/edital.pdf" --engine docling --verbose
```

### Converter todos os PDFs da base de conhecimento
```bash
python converter_pdfs_batch.py "memories" --recursive --engine auto
```

### Converter usando pypdf (rápido)
```bash
python converter_pdf_md.py "documento_simples.pdf" --engine pypdf
```

### Converter com fallback automático
```bash
# Tenta Docling primeiro, usa pypdf se falhar
python converter_pdf_md.py "documento.pdf" --engine auto
```

---

## Integração com Workflow BMAD

O workflow BMAD utiliza automaticamente os scripts de conversão:

1. Quando o usuário digita `INICIAR` ou comando equivalente
2. O sistema converte PDFs da memória organizacional
3. Converte o PDF do edital
4. Lê os arquivos Markdown gerados
5. Incorpora conhecimentos ao projeto

O sistema escolhe automaticamente o melhor engine disponível, garantindo máxima qualidade quando possível e funcionamento mesmo sem Docling instalado.

---

## Estrutura de Diretórios Recomendada

```
memories/
├── ORGANIZATION_PORTFOLIO.md         # Portfólio da organização (Markdown)
├── editais/                          # Editais processados
│   ├── [edital-nome]/
│   │   ├── edital.pdf
│   │   ├── edital.md                 # Gerado automaticamente
│   │   └── projeto/                  
│   │       ├── FASE1_ANALISE.md
│   │       ├── FASE2_PLANEJAMENTO.md
│   │       ├── FASE3_SOLUCAO.md
│   │       ├── FASE4_IMPLEMENTACAO.md
└── logs/
    └── conversao_pdfs_log.txt        # Log de conversões
```

---

**Desenvolvido por:** BMAD Grants Brazil  
**Contexto:** Módulo genérico para elaboração de projetos para editais  
**Data:** Dezembro 2025
