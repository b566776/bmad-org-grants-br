#!/bin/bash
# Script de instalação do bmad-org-grants-br
# Copia scripts Python, configurações e instala dependências

set -e  # Sair se houver erro

echo "🚀 Instalando bmad-org-grants-br..."
echo ""

# Verificar se está no diretório correto
if [[ ! -d "../../.." ]] || [[ ! -f "../../module.yaml" ]]; then
    echo "❌ Erro: Execute este script do diretório _bmad/modules/bmad-org-grants-br"
    echo "   Navegue até o diretório correto e tente novamente."
    exit 1
fi

# Solicitar URL do repositório
read -p "📦 URL do repositório (default: https://github.com/SUA_ORG/bmad-org-grants-br.git): " REPO_URL
REPO_URL=${REPO_URL:-https://github.com/SUA_ORG/bmad-org-grants-br.git}

# Criar diretório temporário
TEMP_DIR="../../../temp-bgb-install"
echo "📥 Clonando repositório..."
git clone "$REPO_URL" "$TEMP_DIR"

if [ $? -ne 0 ]; then
    echo "❌ Erro ao clonar repositório"
    exit 1
fi

echo "📋 Copiando scripts Python..."
cp "$TEMP_DIR/pdf_converter.py" .
cp "$TEMP_DIR/converter_pdf_md.py" .
cp "$TEMP_DIR/converter_pdfs_batch.py" .
cp "$TEMP_DIR/requirements.txt" .

echo "⚙️  Copiando configurações..."
cp -r "$TEMP_DIR/config" .

echo "📚 Copiando documentação..."
cp -r "$TEMP_DIR/docs" .

echo "🧹 Limpando diretório temporário..."
rm -rf "$TEMP_DIR"

echo ""
echo "✅ Arquivos copiados com sucesso!"
echo ""

# Verificar se Python está disponível
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "⚠️  Python não encontrado. Instale Python 3.8+ manualmente."
    echo "   Depois execute: pip install -r requirements.txt"
    exit 0
fi

# Verificar se pip está disponível
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo "⚠️  pip não encontrado. Instale pip manualmente."
    echo "   Depois execute: pip install -r requirements.txt"
    exit 0
fi

# Perguntar se deseja instalar dependências
read -p "📦 Instalar dependências Python agora? (s/N): " INSTALL_DEPS
INSTALL_DEPS=${INSTALL_DEPS:-N}

if [[ "$INSTALL_DEPS" =~ ^[Ss]$ ]]; then
    echo "📦 Instalando dependências Python..."
    $PIP_CMD install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Instalação concluída com sucesso!"
        echo ""
        echo "📋 Próximos passos:"
        echo "   1. Execute: npx bmad-method@alpha install"
        echo "   2. Escolha: 'Compile all agents'"
        echo "   3. Comece a usar o módulo!"
    else
        echo "⚠️  Erro ao instalar dependências."
        echo "   Tente manualmente: $PIP_CMD install -r requirements.txt"
    fi
else
    echo ""
    echo "⚠️  Dependências não instaladas."
    echo "   Execute manualmente: $PIP_CMD install -r requirements.txt"
    echo ""
    echo "📋 Próximos passos:"
    echo "   1. Instale dependências: $PIP_CMD install -r requirements.txt"
    echo "   2. Execute: npx bmad-method@alpha install"
    echo "   3. Escolha: 'Compile all agents'"
fi

echo ""
echo "🎉 Configuração completa!"
