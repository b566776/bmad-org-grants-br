#!/usr/bin/env python3
"""
Script para trocar a organização ativa no módulo BMAD-Editais
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def get_organizations_dir():
    """Retorna o diretório de organizações"""
    script_dir = Path(__file__).parent
    return script_dir.parent / "memories" / "organizations"

def switch_organization(profile_name):
    """Tr oca para a organização especificada"""
    orgs_dir = get_organizations_dir()
    profile_dir = orgs_dir / profile_name
    current_file = orgs_dir / ".current"
    
    # Verificar se perfil existe
    if not profile_dir.exists():
        print(f"❌ Erro: Perfil '{profile_name}' não encontrado")
        print(f"\n💡 Perfis disponíveis:")
        for d in orgs_dir.iterdir():
            if d.is_dir():
                print(f"   - {d.name}")
        return False
    
    # Verificar se tem config.json
    config_file = profile_dir / "config.json"
    if not config_file.exists():
        print(f"⚠️  Aviso: Perfil '{profile_name}' não tem config.json")
        confirm = input("Continuar mesmo assim? (s/N): ")
        if confirm.lower() != 's':
            print("Operação cancelada")
            return False
    
    # Carregar dados da organização
    org_name = profile_name
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        org_name = config.get("organization_name", profile_name)
    
    # Atualizar .current
    current_data = {
        "active_profile": profile_name,
        "last_switched": datetime.now().isoformat(),
        "profiles_count": len([d for d in orgs_dir.iterdir() if d.is_dir()]),
        "version": "1.0"
    }
    
    with open(current_file, 'w', encoding='utf-8') as f:
        json.dump(current_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Organização alterada para: {org_name}")
    print(f"📂 Contexto carregado de: organizations/{profile_name}/")
    print(f"🎯 Pronto para processar editais\n")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("❌ Uso: python switch-organization.py <nome-perfil>")
        print("\n💡 Para ver perfis disponíveis:")
        print("   python list-organizations.py")
        sys.exit(1)
    
    profile_name = sys.argv[1]
    
    try:
        if switch_organization(profile_name):
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
