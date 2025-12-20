#!/usr/bin/env python3
"""
Script para converter PDF em Markdown
Usa Docling (primário) ou pypdf (fallback) via módulo pdf_converter.py
"""

import sys
import argparse
from pathlib import Path

try:
    from pdf_converter import convert_pdf_to_markdown, detect_available_engine
except ImportError:
    print("Erro: Módulo pdf_converter.py não encontrado.", file=sys.stderr)
    print("Certifique-se de que pdf_converter.py está no mesmo diretório.", file=sys.stderr)
    sys.exit(1)


def pdf_to_markdown(pdf_path: str, output_path: str = None, engine: str = None, verbose: bool = False) -> str:
    """
    Converte um PDF para Markdown (função compatível com código existente)
    
    Args:
        pdf_path: Caminho para o arquivo PDF
        output_path: Caminho para salvar o Markdown (opcional)
        engine: Engine a usar ('docling', 'pypdf', 'auto')
        verbose: Se True, mostra informações detalhadas
        
    Returns:
        Caminho do arquivo Markdown gerado
    """
    try:
        result_path, metadata = convert_pdf_to_markdown(
            pdf_path=pdf_path,
            output_path=output_path,
            engine=engine,
            fallback=True,
            verbose=verbose
        )
        
        if verbose:
            engine_used = metadata.get("engine_used", "unknown")
            fallback_used = metadata.get("fallback_used", False)
            
            print(f"\n✅ Conversão concluída!", file=sys.stderr)
            print(f"📄 Arquivo Markdown salvo em: {result_path}", file=sys.stderr)
            print(f"🔧 Engine usado: {engine_used}", file=sys.stderr)
            if fallback_used:
                print(f"⚠️  Fallback foi necessário", file=sys.stderr)
            if metadata.get("total_pages"):
                print(f"📊 Total de páginas processadas: {metadata['total_pages']}", file=sys.stderr)
        
        return result_path
        
    except Exception as e:
        if verbose:
            print(f"\n❌ Erro na conversão: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Converte PDF para Markdown usando Docling ou pypdf",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python converter_pdf_md.py "memories/editais/edital.pdf"
  python converter_pdf_md.py "memories/ORGANIZATION_PORTFOLIO.pdf"
  python converter_pdf_md.py "certidao.pdf" --engine docling
  python converter_pdf_md.py "documento.pdf" --engine pypdf --verbose
        """
    )
    
    parser.add_argument(
        "pdf_path",
        help="Caminho para o arquivo PDF"
    )
    
    parser.add_argument(
        "output_path",
        nargs="?",
        default=None,
        help="Caminho de saída para o arquivo Markdown (opcional)"
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
        help="Mostra informações detalhadas sobre o processo"
    )
    
    args = parser.parse_args()
    
    # Verifica engines disponíveis
    if args.verbose:
        engine_name, is_available = detect_available_engine(args.engine)
        print(f"🔍 Engine detectado: {engine_name} (disponível: {is_available})", file=sys.stderr)
    
    try:
        result = pdf_to_markdown(
            pdf_path=args.pdf_path,
            output_path=args.output_path,
            engine=args.engine,
            verbose=args.verbose
        )
        
        if not args.verbose:
            print(f"✅ Sucesso! Arquivo: {result}")
            
    except FileNotFoundError as e:
        print(f"\n❌ Erro: Arquivo não encontrado", file=sys.stderr)
        print(f"   {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)
