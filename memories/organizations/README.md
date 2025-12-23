# Diretório de Organizações (Multi-Tenant)

Este diretório contém perfis de múltiplas organizações para uso com o módulo BMAD-Editais.

## 📁 Estrutura

```
organizations/
├── .current                    # Arquivo que indica o perfil ativo
│
├── default/                    # Perfil padrão
│   ├── config.json             # Metadados da organização
│   ├── ORGANIZATION_PORTFOLIO.md
│   ├── HISTORICO_EDITAIS.md
│   ├── certidoes/
│   ├── documentos_bancarios/
│   ├── documentos_institucionais/
│   ├── projetos_anteriores/
│   └── logs/
│
├── outra-organizacao/          # Exemplo de outro perfil
│   ├── config.json
│   └── ...
│
└── README.md (este arquivo)
```

## 🎯 Conceito

Cada subdiretório representa uma **organização diferente** com:
- Documentos próprios
- Histórico de editais independente
- Portfolio gerado automaticamente
- Configurações personalizadas

## 🔄 Perfil Ativo

O arquivo `.current` define qual organização está ativa. Os workflows usam automaticamente os dados da organização ativa.

**Conteúdo de `.current`:**
```json
{
  "active_profile": "default",
  "last_switched": "2025-12-23T14:23:37-03:00"
}
```

## 🛠️ Gerenciamento de Perfis

### Listar Organizações Disponíveis

```bash
python scripts/list-organizations.py
```

### Trocar Organização Ativa

```bash
python scripts/switch-organization.py nome-do-perfil
```

### Criar Nova Organização

```bash
python scripts/create-organization.py --name "Nova ONG" --type ngo
```

### Exportar Organização (Backup)

```bash
python scripts/export-organization.py default ./backup/
```

## 📝 Arquivo config.json

Cada perfil deve ter um `config.json` com metadados:

```json
{
  "organization_name": "Nome da Organização",
  "organization_type": "ngo|startup|company|institute",
  "cnpj": "00.000.000/0000-00",
  "created_at": "2025-12-23T14:00:00-03:00",
  "areas_atuacao": ["saúde", "educação"],
  "color": "#1976D2",
  "icon": "🏢"
}
```

## 🚀 Casos de Uso

### Consultor com Múltiplos Clientes

```bash
# Segunda-feira: ONG de Direitos Humanos
python scripts/switch-organization.py ong-direitos-humanos
# Trabalhar normalmente...

# Quarta-feira: Startup de Agritech
python scripts/switch-organization.py startup-agritech
# Trabalhar normalmente...
```

### Backup de Organização Específica

```bash
# Exportar apenas uma organização
python scripts/export-organization.py ong-saude ./backup-ong-saude/
```

### Adicionar Cliente Novo

```bash
# Criar perfil vazio
python scripts/create-organization.py --name "Nova Empresa XYZ" --type company

# OU importar backup existente
python scripts/import-organization.py ./backup-cliente/ --name empresa-xyz
```

## ⚠️ Importante

- ✅ Cada perfil é **totalmente isolado**
- ✅ Workflows usam automaticamente o perfil ativo
- ✅ Nenhum vazamento de dados entre perfis
- ✅ Backup e restore por organização

## 📊 Estrutura de Cada Perfil

Cada perfil deve seguir esta estrutura:

```
{perfil}/
├── config.json                         # Obrigatório
├── ORGANIZATION_PORTFOLIO.md           # Auto-gerado
├── HISTORICO_EDITAIS.md               # Auto-gerado
├── certidoes/                         # Opcional
├── documentos_bancarios/              # Opcional
├── documentos_institucionais/         # Opcional
├── projetos_anteriores/               # Opcional
└── logs/                              # Auto-criado
```

---

**Versão:** 1.0  
**Data:** Dezembro 2025  
**Módulo:** BMAD Grants Brazil
