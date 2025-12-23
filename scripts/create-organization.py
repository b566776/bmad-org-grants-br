#!/usr/bin/env python3
"""
Script para criar uma nova organização no módulo BMAD-Editais
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

def get_organizations_dir():
    """Retorna o diretório de organizações"""
    script_dir = Path(__file__).parent
    return script_dir.parent / "memories" / "organizations"

def create_organization(name, org_type="ngo", cnpj="", interactive=False):
    """Cria uma nova organização"""
    orgs_dir = get_organizations_dir()
    
    # Gerar nome do perfil (slug)
    profile_name = name.lower().replace(" ", "-").replace(".", "")
    profile_name = "".join(c for c in profile_name if c.isalnum() or c == "-")
    
    profile_dir = orgs_dir / profile_name
    
    # Verificar se já existe
    if profile_dir.exists():
        print(f"❌ Erro: Perfil '{profile_name}' já existe")
        return False
    
    print(f"\n📝 Criando perfil de nova organização...")
    print(f"   Nome: {name}")
    print(f"   Perfil: {profile_name}")
    print(f"   Tipo: {org_type}\n")
    
    # Criar diretório do perfil
    profile_dir.mkdir(parents=True, exist_ok=True)
    
    # Criar subdiretórios
    subdirs = [
        "certidoes",
        "documentos_bancarios",
        "documentos_institucionais",
        "projetos_anteriores",
        "logs"
    ]
    
    for subdir in subdirs:
        (profile_dir / subdir).mkdir(exist_ok=True)
    
    # Criar config.json
    config = {
        "organization_name": name,
        "organization_type": org_type,
        "cnpj": cnpj,
        "created_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "description": "",
        "tags": [],
        "areas_atuacao": [],
        "color": "#1976D2",
        "icon": get_icon_for_type(org_type),
        "notes": "Perfil criado via script create-organization.py"
    }
    
    config_file = profile_dir / "config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    # Criar HISTORICO_EDITAIS.md vazio
    historico_content = f"""# Histórico de Editais - {name}

Este arquivo registra todos os editais processados por esta organização.

## 📋 Editais em Andamento

| Edital | Data Início | Prazo Submissão | Status | Pasta |
|--------|-------------|-----------------|--------|-------|
| - | - | - | - | - |

## ✅ Editais Submetidos

| Edital | Data Submissão | Valor Solicitado | Status | Pasta |
|--------|----------------|------------------|--------|-------|
| - | - | - | - | - |

---

**Última atualização:** {datetime.now().strftime("%d/%m/%Y")}
"""
    
    (profile_dir / "HISTORICO_EDITAIS.md").write_text(historico_content, encoding='utf-8')
    
    print(f"✅ Perfil criado: organizations/{profile_name}/")
    print(f"📁 Estrutura de diretórios criada")
    print(f"📄 Arquivos de configuração gerados\n")
    print(f"💡 Próximos passos:")
    print(f"   1. Adicione documentos nas subpastas (certidoes/, documentos_*/, etc.)")
    print(f"   2. Execute: python scripts/switch-organization.py {profile_name}")
    print(f"   3. Execute Fase 1 para gerar o portfolio automaticamente\n")
    
    return True

def get_icon_for_type(org_type):
    """Retorna ícone padrão baseado no tipo"""
    icons = {
        "ngo": "🤝",
        "startup": "🚀",
        "company": "🏢",
        "institute": "🎓",
        "foundation": "🏛️"
    }
    return icons.get(org_type, "🏢")

def main():
    parser = argparse.ArgumentParser(
        description="Criar nova organização no módulo BMAD-Editais"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Nome da organização"
    )
    parser.add_argument(
        "--type",
        default="ngo",
        choices=["ngo", "startup", "company", "institute", "foundation"],
        help="Tipo de organização (padrão: ngo)"
    )
    parser.add_argument(
        "--cnpj",
        default="",
        help="CNPJ da organização (opcional)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Modo interativo (pede confirmação)"
    )
    
    args = parser.parse_args()
    
    try:
        if create_organization(args.name, args.type, args.cnpj, args.interactive):
            exit(0)
        else:
            exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        exit(1)

if __name__ == "__main__":
    main()
