# Script de instalação do bmad-org-grants-br (PowerShell)
# Copia scripts Python, configurações e instala dependências

$ErrorActionPreference = "Stop"

Write-Host "🚀 Instalando bmad-org-grants-br..." -ForegroundColor Cyan
Write-Host ""

# Verificar se está no diretório correto
if (-not (Test-Path "../../..") -or -not (Test-Path "../../module.yaml")) {
    Write-Host "❌ Erro: Execute este script do diretório _bmad/modules/bmad-org-grants-br" -ForegroundColor Red
    Write-Host "   Navegue até o diretório correto e tente novamente." -ForegroundColor Yellow
    exit 1
}

# Solicitar URL do repositório
$repoUrl = Read-Host "📦 URL do repositório (default: https://github.com/SUA_ORG/bmad-org-grants-br.git)"
if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    $repoUrl = "https://github.com/SUA_ORG/bmad-org-grants-br.git"
}

# Criar diretório temporário
$tempDir = "../../../temp-bgb-install"
Write-Host "📥 Clonando repositório..." -ForegroundColor Cyan

try {
    git clone $repoUrl $tempDir
} catch {
    Write-Host "❌ Erro ao clonar repositório: $_" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Copiando scripts Python..." -ForegroundColor Cyan
Copy-Item "$tempDir/pdf_converter.py" . -Force
Copy-Item "$tempDir/converter_pdf_md.py" . -Force
Copy-Item "$tempDir/converter_pdfs_batch.py" . -Force
Copy-Item "$tempDir/requirements.txt" . -Force

Write-Host "⚙️  Copiando configurações..." -ForegroundColor Cyan
Copy-Item "$tempDir/config" -Recurse . -Force

Write-Host "📚 Copiando documentação..." -ForegroundColor Cyan
Copy-Item "$tempDir/docs" -Recurse . -Force

Write-Host "🧹 Limpando diretório temporário..." -ForegroundColor Cyan
Remove-Item $tempDir -Recurse -Force

Write-Host ""
Write-Host "✅ Arquivos copiados com sucesso!" -ForegroundColor Green
Write-Host ""

# Verificar se Python está disponível
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
}

if (-not $pythonCmd) {
    Write-Host "⚠️  Python não encontrado. Instale Python 3.8+ manualmente." -ForegroundColor Yellow
    Write-Host "   Depois execute: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 0
}

# Verificar se pip está disponível
$pipCmd = $null
if (Get-Command pip -ErrorAction SilentlyContinue) {
    $pipCmd = "pip"
} elseif (Get-Command pip3 -ErrorAction SilentlyContinue) {
    $pipCmd = "pip3"
}

if (-not $pipCmd) {
    Write-Host "⚠️  pip não encontrado. Instale pip manualmente." -ForegroundColor Yellow
    Write-Host "   Depois execute: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 0
}

# Perguntar se deseja instalar dependências
$installDeps = Read-Host "📦 Instalar dependências Python agora? (s/N)"
if ($installDeps -match "^[Ss]$") {
    Write-Host "📦 Instalando dependências Python..." -ForegroundColor Cyan
    
    try {
        & $pipCmd install -r requirements.txt
        
        Write-Host ""
        Write-Host "✅ Instalação concluída com sucesso!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📋 Próximos passos:" -ForegroundColor Cyan
        Write-Host "   1. Execute: npx bmad-method@alpha install"
        Write-Host "   2. Escolha: 'Compile all agents'"
        Write-Host "   3. Comece a usar o módulo!"
    } catch {
        Write-Host "⚠️  Erro ao instalar dependências: $_" -ForegroundColor Yellow
        Write-Host "   Tente manualmente: $pipCmd install -r requirements.txt" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "⚠️  Dependências não instaladas." -ForegroundColor Yellow
    Write-Host "   Execute manualmente: $pipCmd install -r requirements.txt" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📋 Próximos passos:" -ForegroundColor Cyan
    Write-Host "   1. Instale dependências: $pipCmd install -r requirements.txt"
    Write-Host "   2. Execute: npx bmad-method@alpha install"
    Write-Host "   3. Escolha: 'Compile all agents'"
}

Write-Host ""
Write-Host "🎉 Configuração completa!" -ForegroundColor Green
