# Features Opcionais - Guia de Uso com IA

> **📌 Para Assistentes de IA**: Este documento contém exemplos de código prontos para execução e prompts claros para facilitar a automação de tarefas.

---

## 1. Sistema de Links Úteis Categorizados

### 📍 Arquivo
`memories/links_uteis.json`

### 📝 Descrição
Base de dados JSON com +50 links organizados em 8 categorias para elaboração de projetos.

---

### 🤖 Prompt para IA: "Buscar Links por Categoria"

**Comando para IA:**
```
Por favor, leia o arquivo memories/links_uteis.json e liste todos os links da categoria "editais_federais"
```

**Código Executável:**
```python
import json
from pathlib import Path

# Ler arquivo de links
links_file = Path("memories/links_uteis.json")
with open(links_file, 'r', encoding='utf-8') as f:
    links_data = json.load(f)

# Acessar categoria específica
categoria = "editais_federais"
links = links_data['categorias'][categoria]['links']

# Exibir links
print(f"\n📂 Categoria: {links_data['categorias'][categoria]['nome']}\n")
for link in links:
    print(f"🔗 {link['titulo']}")
    print(f"   URL: {link['url']}")
    print(f"   {link['descricao']}")
    print()
```

**Saída Esperada:**
```
📂 Categoria: Editais e Plataformas Federais

🔗 Portal de Convênios (SICONV)
   URL: https://www.gov.br/transferegov/pt-br
   Sistema oficial para convênios e parcerias com o governo federal
...
```

---

### 🤖 Prompt para IA: "Buscar Links por Tag"

**Comando para IA:**
```
Crie uma função para buscar todos os links que contenham a tag "inovação" no arquivo memories/links_uteis.json
```

**Código Executável:**
```python
import json
from pathlib import Path

def buscar_por_tag(tag_procurada):
    """Busca links que contenham uma tag específica"""
    links_file = Path("memories/links_uteis.json")
    with open(links_file, 'r', encoding='utf-8') as f:
        links_data = json.load(f)
    
    resultados = []
    for categoria in links_data['categorias'].values():
        for link in categoria['links']:
            if tag_procurada in link.get('tags', []):
                resultados.append({
                    'titulo': link['titulo'],
                    'url': link['url'],
                    'categoria': categoria['nome']
                })
    
    return resultados

# Executar busca
tag = "inovação"
links_encontrados = buscar_por_tag(tag)

print(f"🔍 Encontrados {len(links_encontrados)} links com tag '{tag}':\n")
for link in links_encontrados:
    print(f"• {link['titulo']}")
    print(f"  📂 {link['categoria']}")
    print(f"  🔗 {link['url']}\n")
```

---

### 🤖 Prompt para IA: "Adicionar Novo Link"

**Comando para IA:**
```
Adicione um novo link ao arquivo memories/links_uteis.json:
- Categoria: fundacoes_institutos
- Título: Instituto Ayrton Senna
- URL: https://institutoayrtonsenna.org.br
- Descrição: Fomento à educação e desenvolvimento social
- Tags: educação, social
```

**Código Executável:**
```python
import json
from pathlib import Path

def adicionar_link(categoria, novo_link):
    """Adiciona um novo link à categoria especificada"""
    links_file = Path("memories/links_uteis.json")
    
    # Ler arquivo atual
    with open(links_file, 'r', encoding='utf-8') as f:
        links_data = json.load(f)
    
    # Adicionar novo link
    links_data['categorias'][categoria]['links'].append(novo_link)
    
    # Salvar arquivo atualizado
    with open(links_file, 'w', encoding='utf-8') as f:
        json.dump(links_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Link '{novo_link['titulo']}' adicionado à categoria '{categoria}'")

# Exemplo de uso
novo_link = {
    "titulo": "Instituto Ayrton Senna",
    "url": "https://institutoayrtonsenna.org.br",
    "descricao": "Fomento à educação e desenvolvimento social",
    "tags": ["educação", "social"]
}

adicionar_link("fundacoes_institutos", novo_link)
```

---

## 2. Análise Preditiva de Chances de Aprovação

### 📍 Arquivo
`approval_predictor.py`

### 📝 Descrição
Analisa proposta completa e estima probabilidade de aprovação em 7 critérios ponderados.

---

### 🤖 Prompt para IA: "Executar Análise Preditiva"

**Comando para IA (Simples):**
```
Execute o script approval_predictor.py para analisar a proposta localizada em memories/editais/edital-xyz/projeto/
```

**Comando Shell:**
```bash
python approval_predictor.py memories/editais/edital-xyz/projeto/
```

**Saída Esperada:**
```
======================================================================
📊 ANÁLISE PREDITIVA DE CHANCES DE APROVAÇÃO
======================================================================

🎯 PROBABILIDADE DE APROVAÇÃO: 72.5%
📈 CLASSIFICAÇÃO: MÉDIA-ALTA

📋 SCORES POR CRITÉRIO:
----------------------------------------------------------------------
Coerência Estrutural (DVP)............. ████████████████ 80%
Alinhamento com Edital................. ██████████████ 70%
...
```

---

### 🤖 Prompt para IA: "Análise Programática com Customização"

**Comando para IA:**
```
Crie um script que execute a análise preditiva e envie os resultados por email se a probabilidade for menor que 60%
```

**Código Executável:**
```python
from pathlib import Path
from approval_predictor import ApprovalPredictor, generate_report

def analisar_e_alertar(projeto_dir, threshold=0.60):
    """Analisa proposta e alerta se probabilidade for baixa"""
    
    # Buscar arquivos das fases
    proposal_files = {}
    for fase_num, fase_nome in [
        ("1", "ANALISE"), ("3", "SOLUCAO"), 
        ("4", "IMPLEMENTACAO"), ("5", "VALIDACAO")
    ]:
        fase_file = Path(projeto_dir) / f"FASE{fase_num}_{fase_nome}.md"
        if fase_file.exists():
            proposal_files[f"fase{fase_num}"] = str(fase_file)
    
    # Executar análise
    predictor = ApprovalPredictor()
    analysis = predictor.analyze_proposal(proposal_files)
    
    prob = analysis['overall_probability']
    
    # Gerar relatório
    report = generate_report(analysis)
    print(report)
    
    # Salvar relatório
    report_file = Path(projeto_dir) / "ANALISE_PREDITIVA.md"
    report_file.write_text(report, encoding='utf-8')
    
    # Alerta se probabilidade baixa
    if prob < threshold:
        print(f"\n⚠️  ATENÇÃO: Probabilidade baixa ({prob*100:.1f}%)")
        print(f"🔴 Recomendação: Revisar pontos fracos antes de submeter")
        
        # Aqui você poderia enviar email, Slack, etc.
        # send_alert_email(analysis)
    else:
        print(f"\n✅ Probabilidade adequada ({prob*100:.1f}%)")
    
    return analysis

# Executar
resultado = analisar_e_alertar("memories/editais/edital-xyz/projeto/", threshold=0.60)
```

---

### 🤖 Prompt para IA: "Comparar Múltiplas Propostas"

**Comando para IA:**
```
Compare as chances de aprovação de 3 propostas diferentes e mostre qual tem melhor probabilidade
```

**Código Executável:**
```python
from pathlib import Path
from approval_predictor import ApprovalPredictor

def comparar_propostas(propostas_dirs):
    """Compara múltiplas propostas e rankeia por probabilidade"""
    predictor = ApprovalPredictor()
    resultados = []
    
    for projeto_dir in propostas_dirs:
        # Buscar arquivos
        proposal_files = {}
        for fase_num in ["1", "3", "4", "5"]:
            for fase_nome in ["ANALISE", "SOLUCAO", "IMPLEMENTACAO", "VALIDACAO"]:
                fase_file = Path(projeto_dir) / f"FASE{fase_num}_{fase_nome}.md"
                if fase_file.exists():
                    proposal_files[f"fase{fase_num}"] = str(fase_file)
                    break
        
        # Analisar
        if proposal_files:
            analysis = predictor.analyze_proposal(proposal_files)
            resultados.append({
                'projeto': Path(projeto_dir).name,
                'probabilidade': analysis['overall_probability'],
                'classificacao': analysis['classification']
            })
    
    # Ordenar por probabilidade
    resultados.sort(key=lambda x: x['probabilidade'], reverse=True)
    
    # Exibir ranking
    print("📊 RANKING DE PROPOSTAS\n")
    print("="*60)
    for i, resultado in enumerate(resultados, 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
        print(f"{emoji} #{i} - {resultado['projeto']}")
        print(f"    Probabilidade: {resultado['probabilidade']*100:.1f}%")
        print(f"    Classificação: {resultado['classificacao']}")
        print()
    
    return resultados

# Exemplo de uso
propostas = [
    "memories/editais/edital-a/projeto",
    "memories/editais/edital-b/projeto",
    "memories/editais/edital-c/projeto"
]

ranking = comparar_propostas(propostas)
```

---

### 🤖 Prompt para IA: "Ajustar Pesos dos Critérios"

**Comando para IA:**
```
Modifique o approval_predictor.py para dar mais peso (30%) ao critério de "Alinhamento com Edital" e menos peso ao DVP (20%)
```

**Código para Editar:**

Localize a classe `ApprovalPredictor` no arquivo `approval_predictor.py`:

```python
# EM: approval_predictor.py, linha ~14
class ApprovalPredictor:
    def __init__(self):
        self.weights = {
            "dvp_score": 0.20,           # ALTERADO: era 0.25
            "alignment_score": 0.30,     # ALTERADO: era 0.20
            "budget_adequacy": 0.15,
            "team_qualification": 0.15,
            "innovation": 0.10,
            "social_impact": 0.05,       # AJUSTADO: era 0.10
            "sustainability": 0.05
        }
```

**Prompt Direto:**
```
Abra approval_predictor.py e altere os pesos em self.weights para:
- dvp_score: 0.20
- alignment_score: 0.30
- budget_adequacy: 0.15
- team_qualification: 0.15
- innovation: 0.10
- social_impact: 0.05
- sustainability: 0.05
```

---

### 🤖 Prompt para IA: "Gerar Dashboard de Análise"

**Comando para IA:**
```
Crie um script que gere um relatório markdown com gráficos ASCII mostrando os scores de todos os critérios de forma visual
```

**Código Executável:**
```python
from approval_predictor import ApprovalPredictor

def gerar_dashboard_ascii(projeto_dir):
    """Gera dashboard visual em ASCII com todos os scores"""
    from pathlib import Path
    
    # Buscar arquivos
    proposal_files = {}
    for fase_num, fase_nome in [("1", "ANALISE"), ("3", "SOLUCAO"), ("4", "IMPLEMENTACAO"), ("5", "VALIDACAO")]:
        fase_file = Path(projeto_dir) / f"FASE{fase_num}_{fase_nome}.md"
        if fase_file.exists():
            proposal_files[f"fase{fase_num}"] = str(fase_file)
    
    # Analisar
    predictor = ApprovalPredictor()
    analysis = predictor.analyze_proposal(proposal_files)
    
    # Gerar dashboard
    dashboard = []
    dashboard.append("# 📊 DASHBOARD DE ANÁLISE PREDITIVA\n")
    dashboard.append(f"**Projeto:** {Path(projeto_dir).parent.name}\n")
    dashboard.append(f"**Probabilidade Geral:** {analysis['overall_probability']*100:.1f}%\n")
    dashboard.append(f"**Classificação:** {analysis['classification']}\n")
    dashboard.append("\n---\n")
    dashboard.append("## 📈 Scores por Critério\n")
    
    # Gráficos ASCII
    for criterion, score in sorted(analysis["scores"].items(), key=lambda x: x[1], reverse=True):
        name_map = {
            "dvp_score": "Coerência Estrutural (DVP)",
            "alignment_score": "Alinhamento com Edital",
            "budget_adequacy": "Adequação Orçamentária",
            "team_qualification": "Qualificação da Equipe",
            "innovation": "Inovação",
            "social_impact": "Impacto Social",
            "sustainability": "Sustentabilidade"
        }
        
        name = name_map.get(criterion, criterion)
        filled = int(score * 30)  # 30 caracteres de largura
        empty = 30 - filled
        bar = "█" * filled + "░" * empty
        
        dashboard.append(f"### {name}\n")
        dashboard.append(f"`{bar}` **{score*100:.0f}%**\n")
    
    dashboard.append("\n---\n")
    dashboard.append("## ✅ Pontos Fortes\n")
    for strength in analysis['strengths']:
        dashboard.append(f"- {strength}\n")
    
    dashboard.append("\n## ⚠️  Pontos Fracos\n")
    for weakness in analysis['weaknesses']:
        dashboard.append(f"- {weakness}\n")
    
    dashboard.append("\n## 💡 Recomendações\n")
    for rec in analysis['recommendations']:
        dashboard.append(f"- {rec}\n")
    
    content = "".join(dashboard)
    
    # Salvar
    output_file = Path(projeto_dir) / "DASHBOARD_ANALISE.md"
    output_file.write_text(content, encoding='utf-8')
    
    print(content)
    print(f"\n💾 Dashboard salvo em: {output_file}")

# Executar
gerar_dashboard_ascii("memories/editais/edital-xyz/projeto/")
```

---

## 🎯 Prompts Rápidos para IA

### Categoria: Links Úteis

1. **"Liste todos os links de dados e indicadores"**
   ```python
   # A IA deve ler memories/links_uteis.json e filtrar categoria "dados_indicadores"
   ```

2. **"Adicione um link do BNDES à categoria fundacoes_institutos"**
   ```python
   # A IA deve editar memories/links_uteis.json
   ```

3. **"Encontre todos os links relacionados a 'ODS'"**
   ```python
   # A IA deve buscar por tag "ODS" ou termo na descrição
   ```

### Categoria: Análise Preditiva

1. **"Analise o projeto em memories/editais/X e me diga se devo submeter"**
   ```bash
   python approval_predictor.py memories/editais/X/projeto/
   ```

2. **"Qual critério está mais fraco na minha proposta?"**
   ```python
   # A IA deve executar análise e identificar score mais baixo
   ```

3. **"Compare minha proposta com propostas anteriores aprovadas"**
   ```python
   # A IA deve analisar múltiplas propostas e comparar
   ```

---

## 🛠️ Dicas para Assistentes de IA

### Ao Executar Código Python:

1. **Sempre verificar se arquivo existe:**
   ```python
   from pathlib import Path
   if not Path("caminho/arquivo").exists():
       print("❌ Arquivo não encontrado")
       return
   ```

2. **Usar caminhos relativos ao workspace:**
   ```python
   # Bom
   Path("memories/links_uteis.json")
   
   # Evitar
   Path("C:/Users/User/Documents/.../links_uteis.json")
   ```

3. **Sempre exibir progresso:**
   ```python
   print(f"🔄 Processando...")
   # código
   print(f"✅ Concluído!")
   ```

### Ao Modificar Arquivos:

1. **Sempre fazer backup antes de editar**
2. **Validar JSON após modificação**
3. **Confirmar com usuário antes de sobrescrever**

---

## 📚 Documentação Adicional

- **README geral**: [../README.md](../README.md)
- **Implementação**: [../IMPLEMENTATION_GUIDE.md](../IMPLEMENTATION_GUIDE.md)
- **Protocolo DVP**: [DAVID_DVP_PROTOCOL.md](./DAVID_DVP_PROTOCOL.md)

---

**Otimizado para:** Cursor IDE, Antigravity, GitHub Copilot  
**Versão:** 2.0 (AI-Friendly)  
**Data:** Dezembro 2025
