#!/usr/bin/env python3
"""
Análise Preditiva de Chances de Aprovação
Avalia uma proposta e estima probabilidade de aprovação baseado em critérios históricos
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import re

# Garantir UTF-8 no Windows (evita UnicodeEncodeError com emojis)
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


class ApprovalPredictor:
    """Analisador preditivo de chances de aprovação de propostas"""
    
    def __init__(self):
        self.weights = {
            "evl_gate_score": 0.25,      # Validação determinística (EVL-like)
            "alignment_score": 0.20,     # Alinhamento com edital
            "budget_adequacy": 0.15,     # Adequação orçamentária
            "team_qualification": 0.15,  # Qualificação da equipe
            "innovation": 0.10,          # Nível de inovação
            "social_impact": 0.10,       # Impacto social esperado
            "sustainability": 0.05       # Sustentabilidade do projeto
        }
        
        self.thresholds = {
            "high": 0.75,      # Alta chance (>75%)
            "medium": 0.60,    # Média chance (60-75%)
            "low": 0.45        # Baixa chance (45-60%)
            # Abaixo de 45% = Muito baixa
        }
    
    def analyze_proposal(self, proposal_files: Dict[str, str], project_dir: Path = None) -> Dict:
        """
        Analisa uma proposta completa e retorna probabilidade de aprovação
        
        Args:
            proposal_files: Dicionário com caminhos dos arquivos das fases
                {
                    "fase1": "path/to/FASE1_ANALISE.md",
                    "fase3": "path/to/FASE3_SOLUCAO.md",
                    "fase4": "path/to/FASE4_IMPLEMENTACAO.md",
                    "fase5": "path/to/FASE5_VALIDACAO.md"
                }
        
        Returns:
            Dicionário com análise completa
        """
        results = {
            "scores": {},
            "overall_probability": 0.0,
            "classification": "",
            "strengths": [],
            "weaknesses": [],
            "recommendations": []
        }
        
        # 1. Analisar Gate EVL-like (validação determinística)
        base_dir = project_dir
        if base_dir is None:
            # Tenta inferir do arquivo de fase 5 (ou de qualquer arquivo disponível)
            for k in ["fase5", "fase4", "fase3", "fase1"]:
                if k in proposal_files:
                    base_dir = Path(proposal_files[k]).parent
                    break
        if base_dir is not None:
            results["scores"]["evl_gate_score"] = self._analyze_evl_gate_score(base_dir)
        
        # 2. Analisar alinhamento com edital (Fase 1)
        if "fase1" in proposal_files:
            results["scores"]["alignment_score"] = self._analyze_alignment(
                proposal_files["fase1"]
            )
        
        # 3. Analisar adequação orçamentária (Fase 4)
        if "fase4" in proposal_files:
            results["scores"]["budget_adequacy"] = self._analyze_budget(
                proposal_files["fase4"]
            )
        
        # 4. Analisar qualificação da equipe (Fase 4)
        if "fase4" in proposal_files:
            results["scores"]["team_qualification"] = self._analyze_team(
                proposal_files["fase4"]
            )
        
        # 5. Analisar inovação (Fase 3)
        if "fase3" in proposal_files:
            results["scores"]["innovation"] = self._analyze_innovation(
                proposal_files["fase3"]
            )
        
        # 6. Analisar impacto social (Fase 3)
        if "fase3" in proposal_files:
            results["scores"]["social_impact"] = self._analyze_social_impact(
                proposal_files["fase3"]
            )
        
        # 7. Analisar sustentabilidade (Fase 3)
        if "fase3" in proposal_files:
            results["scores"]["sustainability"] = self._analyze_sustainability(
                proposal_files["fase3"]
            )
        
        # Calcular probabilidade geral
        results["overall_probability"] = self._calculate_overall_score(
            results["scores"]
        )
        
        # Classificar
        results["classification"] = self._classify_probability(
            results["overall_probability"]
        )
        
        # Identificar pontos fortes e fracos
        results["strengths"], results["weaknesses"] = self._identify_strengths_weaknesses(
            results["scores"]
        )
        
        # Gerar recomendações
        results["recommendations"] = self._generate_recommendations(
            results["scores"], results["weaknesses"]
        )
        
        return results
    
    def _analyze_evl_gate_score(self, project_dir: Path) -> float:
        """
        Extrai um score (0..1) do gate EVL-like.
        
        Regra:
        - Se houver erros: score = 0.0 (bloqueante)
        - Se não houver erros: score decresce levemente com warnings
        """
        try:
            fase5 = project_dir / "FASE5_VALIDACAO.md"
            if fase5.exists():
                content = fase5.read_text(encoding="utf-8", errors="ignore")
                low = content.lower()

                # Status explícito
                if "status" in low and "fail" in low:
                    return 0.0
                if "status" in low and "pass" in low:
                    # tenta extrair contagens "Erros:" e "Avisos:"
                    m_err = re.search(r"erros?\\s*\\(?.*?\\)?\\s*:\\s*(\\d+)", low)
                    m_warn = re.search(r"avisos?\\s*:\\s*(\\d+)", low)
                    errors = int(m_err.group(1)) if m_err else 0
                    warnings = int(m_warn.group(1)) if m_warn else 0
                    if errors > 0:
                        return 0.0
                    penalty = min(0.30, warnings * 0.05)
                    return max(0.70, 1.0 - penalty)

                # Sem status claro, mas existe: assume executado com menor confiança
                return 0.70

            # Sem relatório: score neutro (não bloqueia, mas reduz confiança)
            return 0.60
        except Exception:
            return 0.60
    
    def _analyze_alignment(self, filepath: str) -> float:
        """Analisa alinhamento com objetivos do edital"""
        try:
            content = Path(filepath).read_text(encoding='utf-8').lower()
            
            score = 0.5  # Base
            
            # Indicadores de bom alinhamento
            if "atende" in content and "requisitos" in content:
                score += 0.1
            if "elegível" in content or "elegibilidade" in content:
                score += 0.1
            if "pontuação" in content:
                score += 0.1
            if "go" in content and ("no-go" not in content):
                score += 0.2
            
            return min(score, 1.0)
        except:
            return 0.6
    
    def _analyze_budget(self, filepath: str) -> float:
        """Analisa adequação do orçamento"""
        try:
            content = Path(filepath).read_text(encoding='utf-8')
            
            score = 0.5
            
            # Procurar por orçamento detalhado
            if "orçamento" in content.lower():
                score += 0.1
            
            # Verificar se tem categorias de despesa
            categories = ["pessoal", "material", "serviço", "equipamento"]
            for cat in categories:
                if cat in content.lower():
                    score += 0.05
            
            # Verificar se tem justificativa
            if "justificat" in content.lower() and "orçament" in content.lower():
                score += 0.15
            
            return min(score, 1.0)
        except:
            return 0.6
    
    def _analyze_team(self, filepath: str) -> float:
        """Analisa qualificação da equipe"""
        try:
            content = Path(filepath).read_text(encoding='utf-8').lower()
            
            score = 0.5
            
            # Indicadores de boa equipe
            if "coordenador" in content or "coordenação" in content:
                score += 0.1
            if "qualificação" in content or "currículo" in content:
                score += 0.1
            if "experiência" in content:
                score += 0.1
            if "equipe técnica" in content:
                score += 0.1
            
            # Contabilizar membros da equipe (heurística)
            team_indicators = content.count("responsável")
            if team_indicators >= 3:
                score += 0.1
            
            return min(score, 1.0)
        except:
            return 0.6
    
    def _analyze_innovation(self, filepath: str) -> float:
        """Analisa nível de inovação"""
        try:
            content = Path(filepath).read_text(encoding='utf-8').lower()
            
            score = 0.5
            
            # Palavras-chave de inovação
            innovation_keywords = [
                "inovação", "inovador", "novo", "inédito", 
                "tecnologia", "metodologia inovadora", "abordagem diferenciada"
            ]
            
            for keyword in innovation_keywords:
                if keyword in content:
                    score += 0.07
            
            return min(score, 1.0)
        except:
            return 0.5
    
    def _analyze_social_impact(self, filepath: str) -> float:
        """Analisa impacto social esperado"""
        try:
            content = Path(filepath).read_text(encoding='utf-8').lower()
            
            score = 0.5
            
            # Indicadores de impacto social
            if "beneficiários" in content:
                score += 0.1
            if "impacto social" in content or "transformação social" in content:
                score += 0.15
            if "ods" in content or "objetivos de desenvolvimento" in content:
                score += 0.1
            if "indicadores" in content:
                score += 0.1
            
            # Verificar quantificação de beneficiários
            if re.search(r'\d+\s*(pessoas|beneficiários|famílias)', content):
                score += 0.05
            
            return min(score, 1.0)
        except:
            return 0.6
    
    def _analyze_sustainability(self, filepath: str) -> float:
        """Analisa sustentabilidade do projeto"""
        try:
            content = Path(filepath).read_text(encoding='utf-8').lower()
            
            score = 0.5
            
            # Indicadores de sustentabilidade
            if "sustentabilidade" in content:
                score += 0.2
            if "continuidade" in content:
                score += 0.1
            if "longo prazo" in content:
                score += 0.1
            if "parcerias" in content or "parceiros" in content:
                score += 0.1
            
            return min(score, 1.0)
        except:
            return 0.5
    
    def _calculate_overall_score(self, scores: Dict[str, float]) -> float:
        """Calcula probabilidade geral ponderada"""
        total = 0.0
        total_weight = 0.0
        
        for criterion, score in scores.items():
            if criterion in self.weights:
                total += score * self.weights[criterion]
                total_weight += self.weights[criterion]
        
        if total_weight > 0:
            return total / total_weight
        return 0.5
    
    def _classify_probability(self, probability: float) -> str:
        """Classifica a probabilidade em categorias"""
        if probability >= self.thresholds["high"]:
            return "ALTA"
        elif probability >= self.thresholds["medium"]:
            return "MÉDIA-ALTA"
        elif probability >= self.thresholds["low"]:
            return "MÉDIA"
        else:
            return "BAIXA"
    
    def _identify_strengths_weaknesses(
        self, scores: Dict[str, float]
    ) -> Tuple[List[str], List[str]]:
        """Identifica pontos fortes e fracos"""
        strengths = []
        weaknesses = []
        
        criterion_names = {
            "evl_gate_score": "Validação EVL-like (gate)",
            "alignment_score": "Alinhamento com Edital",
            "budget_adequacy": "Adequação Orçamentária",
            "team_qualification": "Qualificação da Equipe",
            "innovation": "Inovação",
            "social_impact": "Impacto Social",
            "sustainability": "Sustentabilidade"
        }
        
        for criterion, score in scores.items():
            name = criterion_names.get(criterion, criterion)
            if score >= 0.75:
                strengths.append(f"{name} ({score*100:.0f}%)")
            elif score < 0.60:
                weaknesses.append(f"{name} ({score*100:.0f}%)")
        
        return strengths, weaknesses
    
    def _generate_recommendations(
        self, scores: Dict[str, float], weaknesses: List[str]
    ) -> List[str]:
        """Gera recomendações baseadas nos pontos fracos"""
        recommendations = []
        
        for criterion, score in scores.items():
            if score < 0.60:
                if criterion == "evl_gate_score":
                    recommendations.append(
                        "🔴 CRÍTICO: Gate EVL-like falhou (ou não foi executado) — corrija erros e revalide antes de submeter"
                    )
                elif criterion == "alignment_score":
                    recommendations.append(
                        "🟠 IMPORTANTE: Revisar alinhamento com objetivos do edital"
                    )
                elif criterion == "budget_adequacy":
                    recommendations.append(
                        "🟡 Detalhar mais o orçamento com justificativas por item"
                    )
                elif criterion == "team_qualification":
                    recommendations.append(
                        "🟡 Incluir currículos ou qualificações mais detalhadas da equipe"
                    )
                elif criterion == "innovation":
                    recommendations.append(
                        "🟢 Destacar aspectos inovadores da metodologia ou abordagem"
                    )
                elif criterion == "social_impact":
                    recommendations.append(
                        "🟡 Quantificar melhor beneficiários e impactos esperados"
                    )
                elif criterion == "sustainability":
                    recommendations.append(
                        "🟡 Elaborar plano de sustentabilidade pós-projeto"
                    )
        
        if not recommendations:
            recommendations.append(
                "✅ Proposta está bem estruturada em todos os critérios analisados"
            )
        
        return recommendations


def generate_report(analysis: Dict) -> str:
    """Gera relatório textual da análise"""
    report = []
    report.append("=" * 70)
    report.append("📊 ANÁLISE PREDITIVA DE CHANCES DE APROVAÇÃO")
    report.append("=" * 70)
    report.append("")
    
    # Probabilidade geral
    prob = analysis["overall_probability"]
    classification = analysis["classification"]
    
    report.append(f"🎯 PROBABILIDADE DE APROVAÇÃO: {prob*100:.1f}%")
    report.append(f"📈 CLASSIFICAÇÃO: {classification}")
    report.append("")
    
    # Scores detalhados
    report.append("📋 SCORES POR CRITÉRIO:")
    report.append("-" * 70)
    
    criterion_names = {
        "evl_gate_score": "Validação EVL-like (gate)",
        "alignment_score": "Alinhamento com Edital",
        "budget_adequacy": "Adequação Orçamentária",
        "team_qualification": "Qualificação da Equipe",
        "innovation": "Inovação",
        "social_impact": "Impacto Social",
        "sustainability": "Sustentabilidade"
    }
    
    for criterion, score in sorted(
        analysis["scores"].items(), 
        key=lambda x: x[1], 
        reverse=True
    ):
        name = criterion_names.get(criterion, criterion)
        bar = "█" * int(score * 20)
        report.append(f"{name:.<40} {bar} {score*100:.0f}%")
    
    report.append("")
    
    # Pontos fortes
    if analysis["strengths"]:
        report.append("✅ PONTOS FORTES:")
        for strength in analysis["strengths"]:
            report.append(f"   • {strength}")
        report.append("")
    
    # Pontos fracos
    if analysis["weaknesses"]:
        report.append("⚠️  PONTOS FRACOS:")
        for weakness in analysis["weaknesses"]:
            report.append(f"   • {weakness}")
        report.append("")
    
    # Recomendações
    report.append("💡 RECOMENDAÇÕES:")
    for rec in analysis["recommendations"]:
        report.append(f"   {rec}")
    
    report.append("")
    report.append("=" * 70)
    
    return "\n".join(report)


def main():
    """Função principal CLI"""
    if len(sys.argv) < 2:
        print("Uso: python approval_predictor.py <diretorio_projeto>")
        print("Exemplo: python approval_predictor.py memories/editais/edital-xyz/projeto")
        sys.exit(1)
    
    project_dir = Path(sys.argv[1])
    
    if not project_dir.exists():
        print(f"❌ Erro: Diretório não encontrado: {project_dir}")
        sys.exit(1)
    
    # Buscar arquivos das fases
    proposal_files = {}
    
    for fase in ["FASE1_ANALISE", "FASE3_SOLUCAO", "FASE4_IMPLEMENTACAO", "FASE5_VALIDACAO"]:
        fase_file = project_dir / f"{fase}.md"
        if fase_file.exists():
            key = fase.lower().replace("_", "").replace("analise", "1").replace("solucao", "3").replace("implementacao", "4").replace("validacao", "5")
            key = f"fase{key[-1]}"  # fase1, fase3, fase4, fase5
            proposal_files[key] = str(fase_file)
    
    if not proposal_files:
        print(f"❌ Erro: Nenhum arquivo de fase encontrado em {project_dir}")
        sys.exit(1)
    
    print(f"📁 Analisando proposta em: {project_dir}")
    print(f"📄 Arquivos encontrados: {len(proposal_files)}")
    print("")
    
    # Executar análise
    predictor = ApprovalPredictor()
    analysis = predictor.analyze_proposal(proposal_files, project_dir=project_dir)
    
    # Gerar relatório
    report = generate_report(analysis)
    print(report)
    
    # Salvar relatório
    report_file = project_dir / "ANALISE_PREDITIVA.md"
    report_file.write_text(report, encoding='utf-8')
    print(f"\n💾 Relatório salvo em: {report_file}")


if __name__ == "__main__":
    main()
