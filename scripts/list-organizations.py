#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para listar organizações disponíveis no módulo BMAD-Editais
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Fix encoding for Windows console
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def get_organizations_dir():
    """Retorna o diretório de organizações"""
    script_dir = Path(__file__).parent
    return script_dir.parent / "memories" / "organizations"

def load_current():
    """Carrega informações do perfil ativo"""
    orgs_dir = get_organizations_dir()
    current_file = orgs_dir / ".current"
    
    if current_file.exists():
        with open(current_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"active_profile": "default"}

def list_organizations():
    """Lista todas as organizações disponíveis"""
    orgs_dir = get_organizations_dir()
    current = load_current()
    active_profile = current.get("active_profile", "default")
    
    print("\n📋 Organizações Disponíveis:\n")
    print("=" * 70)
    
    if not orgs_dir.exists():
        print("⚠️  Diretório de organizações não encontrado")
        return
    
    # Listar todos os diretórios (perfis)
    profiles = [d for d in orgs_dir.iterdir() if d.is_dir()]
    
    if not profiles:
        print("⚠️  Nenhuma organização encontrada")
        return
    
    for profile_dir in sorted(profiles):
        profile_name = profile_dir.name
        config_file = profile_dir / "config.json"
        
        # Indicador de perfil ativo
        is_active = (profile_name == active_profile)
        marker = "  ✅ " if is_active else "     "
        
        # Carregar configuração
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            icon = config.get("icon", "🏢")
            org_name = config.get("organization_name", profile_name)
            org_type = config.get("organization_type", "ngo")
            cnpj = config.get("cnpj", "N/A")
            
            # Contar editais
            editais_count = 0
            # TODO: Implementar contagem real de editais
            
            print(f"{marker}{icon} {profile_name}{'  (ATIVA)' if is_active else ''}")
            print(f"     {org_name}")
            if cnpj and cnpj != "N/A":
                print(f"     CNPJ: {cnpj}")
            print(f"     Tipo: {org_type}")
            # print(f"     Editais: {editais_count}")
            print()
        else:
            print(f"{marker}📁 {profile_name}{'  (ATIVA)' if is_active else ''}")
            print(f"     ⚠️  Sem config.json")
            print()
    
    print("=" * 70)
    print(f"\n💡 Para trocar: python scripts/switch-organization.py <nome-perfil>")
    print(f"💡 Para criar: python scripts/create-organization.py --name \"Nome\"")
    print()

if __name__ == "__main__":
    try:
        list_organizations()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        exit(1)
