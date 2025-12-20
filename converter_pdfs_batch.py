#!/usr/bin/env python3
"""
Script para converter PDFs em Markdown em lote
Mantém log de conversões para evitar reprocessamento
Usa Docling (primário) ou pypdf (fallback) via módulo pdf_converter.py
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

try:
    from pdf_converter import convert_pdf_to_markdown, detect_available_engine
except ImportError:
    print("Erro: Módulo pdf_converter.py não encontrado.", file=sys.stderr)
    print("Certifique-se de que pdf_converter.py está no mesmo diretório.", file=sys.stderr)
    sys.exit(1)


LOG_FILE = "memories/logs/conversao_pdfs_log.txt"


def load_conversion_log() -> dict:
    """Carrega o log de conversões"""
    log_path = Path(LOG_FILE)
    if not log_path.exists():
        return {}
    
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            log_data = {}
            for line in f:
                line = line.strip()
                if line and '|' in line and not line.startswith('#'):
                    parts = line.split('|')
                    if len(parts) >= 3:
                        pdf_path = parts[0].strip()
                        md_path = parts[1].strip()
                        timestamp = parts[2].strip()
                        engine = parts[3].strip() if len(parts) > 3 else "unknown"
                        log_data[pdf_path] = {
                            'md_path': md_path,
                            'timestamp': timestamp,
                            'engine': engine
                        }
        return log_data
    except Exception as e:
        print(f"Aviso: Erro ao carregar log: {e}", file=sys.stderr)
        return {}


def save_conversion_log(log_data: dict):
    """Salva o log de conversões"""
    log_path = Path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("# Log de Conversões PDF -> Markdown\n")
            f.write("# Formato: PDF_PATH | MD_PATH | TIMESTAMP | ENGINE\n")
            f.write("# " + "="*70 + "\n")
            for pdf_path, info in sorted(log_data.items()):
                engine = info.get('engine', 'unknown')
                f.write(f"{pdf_path}|{info['md_path']}|{info['timestamp']}|{engine}\n")
    except Exception as e:
        print(f"Erro ao salvar log: {e}", file=sys.stderr)


def is_pdf_newer_than_md(pdf_path: Path, md_path: Path) -> bool:
    """Verifica se o PDF é mais recente que o MD"""
    if not pdf_path.exists() or not md_path.exists():
        return True
    
    pdf_mtime = pdf_path.stat().st_mtime
    md_mtime = md_path.stat().st_mtime
    return pdf_mtime > md_mtime


def pdf_to_markdown(pdf_path: str, output_path: str = None, engine: str = None, verbose: bool = False) -> tuple:
    """
    Converte um PDF para Markdown usando pdf_converter
    
    Args:
        pdf_path: Caminho para o arquivo PDF
        output_path: Caminho para salvar o Markdown (opcional)
        engine: Engine a usar ('docling', 'pypdf', 'auto')
        verbose: Se True, mostra informações detalhadas
        
    Returns:
        Tupla (caminho_md, metadata)
    """
    try:
        result_path, metadata = convert_pdf_to_markdown(
            pdf_path=pdf_path,
            output_path=output_path,
            engine=engine,
            fallback=True,
            verbose=verbose
        )
        return result_path, metadata
    except Exception as e:
        if verbose:
            print(f"Erro ao converter {pdf_path}: {e}", file=sys.stderr)
        raise


def convert_pdfs_in_directory(
    directory: str,
    recursive: bool = False,
    engine: str = "auto",
    verbose: bool = False
) -> dict:
    """
    Converte todos os PDFs de um diretório
    
    Args:
        directory: Diretório a processar
        recursive: Se True, processa subdiretórios
        engine: Engine a usar ('docling', 'pypdf', 'auto')
        verbose: Se True, mostra informações detalhadas
        
    Returns:
        Dicionário com estatísticas: {'convertidos': int, 'já_existiam': int, 'erros': int, 'engines': dict}
    """
    log_data = load_conversion_log()
    stats = {
        'convertidos': 0,
        'já_existiam': 0,
        'erros': 0,
        'engines': {}
    }
    
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"Diretório não encontrado: {directory}", file=sys.stderr)
        return stats
    
    # Busca PDFs
    if recursive:
        pdf_files = list(dir_path.rglob("*.pdf"))
    else:
        pdf_files = list(dir_path.glob("*.pdf"))
    
    print(f"Encontrados {len(pdf_files)} arquivos PDF em {directory}", file=sys.stderr)
    
    for pdf_file in pdf_files:
        try:
            pdf_str = str(pdf_file.relative_to(Path.cwd()))
        except ValueError:
            # Se não conseguir caminho relativo, usa caminho absoluto
            pdf_str = str(pdf_file)
        md_file = pdf_file.with_suffix('.md')
        try:
            md_str = str(md_file.relative_to(Path.cwd()))
        except ValueError:
            md_str = str(md_file)
        
        # Verifica se já foi convertido e se o MD ainda é válido
        if pdf_str in log_data:
            logged_md = Path(log_data[pdf_str]['md_path'])
            if logged_md.exists() and not is_pdf_newer_than_md(pdf_file, logged_md):
                if verbose:
                    print(f"⏭️  Pulando (já convertido): {pdf_file.name}", file=sys.stderr)
                stats['já_existiam'] += 1
                continue
        
        # Verifica se MD existe e é mais recente
        if md_file.exists() and not is_pdf_newer_than_md(pdf_file, md_file):
            if verbose:
                print(f"⏭️  Pulando (MD atualizado): {pdf_file.name}", file=sys.stderr)
            stats['já_existiam'] += 1
            # Atualiza log mesmo que já exista
            log_data[pdf_str] = {
                'md_path': md_str,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'engine': 'unknown'
            }
            continue
        
        # Converte
        try:
            print(f"🔄 Convertendo: {pdf_file.name}", file=sys.stderr)
            result_md, metadata = pdf_to_markdown(
                str(pdf_file),
                engine=engine,
                verbose=verbose
            )
            
            engine_used = metadata.get("engine_used", "unknown")
            log_data[pdf_str] = {
                'md_path': result_md,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'engine': engine_used
            }
            
            # Atualiza estatísticas de engines
            if engine_used not in stats['engines']:
                stats['engines'][engine_used] = 0
            stats['engines'][engine_used] += 1
            
            stats['convertidos'] += 1
            print(f"✅ Convertido: {pdf_file.name} -> {Path(result_md).name} [{engine_used}]", file=sys.stderr)
        except Exception as e:
            print(f"❌ Erro ao converter {pdf_file.name}: {e}", file=sys.stderr)
            stats['erros'] += 1
    
    # Salva log
    save_conversion_log(log_data)
    
    return stats


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="Converte PDFs em Markdown em lote usando Docling ou pypdf",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python converter_pdfs_batch.py "memories"
  python converter_pdfs_batch.py "memories/editais" --recursive
  python converter_pdfs_batch.py "memories" --engine docling --verbose
        """
    )
    
    parser.add_argument(
        "directory",
        help="Diretório a processar"
    )
    
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="Processa subdiretórios recursivamente"
    )
    
    parser.add_argument(
        "--engine",
        choices=["docling", "pypdf", "auto"],
        default="auto",
        help="Engine de conversão a usar (padrão: auto)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostra informações detalhadas"
    )
    
    args = parser.parse_args()
    
    # Por padrão, usa recursivo para memories (tem subpastas)
    recursive = args.recursive or 'memories' in args.directory
    
    print(f"🔄 Iniciando conversão de PDFs em: {args.directory}", file=sys.stderr)
    if recursive:
        print("📂 Modo recursivo ativado", file=sys.stderr)
    
    # Verifica engines disponíveis
    if args.verbose:
        engine_name, is_available = detect_available_engine(args.engine)
        print(f"🔍 Engine detectado: {engine_name} (disponível: {is_available})", file=sys.stderr)
    
    stats = convert_pdfs_in_directory(
        args.directory,
        recursive=recursive,
        engine=args.engine,
        verbose=args.verbose
    )
    
    print("\n" + "="*50, file=sys.stderr)
    print("📊 RESUMO DA CONVERSÃO", file=sys.stderr)
    print("="*50, file=sys.stderr)
    print(f"✅ Convertidos: {stats['convertidos']}", file=sys.stderr)
    print(f"⏭️  Já existiam: {stats['já_existiam']}", file=sys.stderr)
    print(f"❌ Erros: {stats['erros']}", file=sys.stderr)
    
    if stats['engines']:
        print("\n🔧 Engines utilizados:", file=sys.stderr)
        for engine, count in stats['engines'].items():
            print(f"   {engine}: {count}", file=sys.stderr)
    
    print("="*50, file=sys.stderr)
    
    # Retorna JSON para uso programático
    print(json.dumps(stats))


if __name__ == "__main__":
    main()
