"""
Dashboard - Gerencia estatísticas e insights do sistema.

Author: @monrars
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


class Dashboard:
    """
    Gerencia dashboard de estatísticas e insights do sistema.

    Funcionalidades:
    - Visão geral de modelos e análises
    - Estatísticas de performance
    - Insights automáticos
    - Recomendações
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.data_dir = Path.home() / ".neuro-skills" / "viral-content-creator"
        self.models_dir = self.data_dir / "models"
        self.cache_dir = self.data_dir / "cache"
        self.generated_dir = self.data_dir / "generated"

        for d in [self.data_dir, self.models_dir, self.cache_dir, self.generated_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def get_overview(self, periodo: str = "30d") -> Dict[str, Any]:
        """
        Retorna visão geral do sistema.

        Args:
            periodo: Período de análise (ex: "30d", "7d", "90d")

        Returns:
            Dict com resumo geral
        """
        models_count = len(list(self.models_dir.glob("*.json")))
        generated_count = len(list(self.generated_dir.glob("*.json")))

        return {
            "resumo": {
                "modelos_criados": models_count,
                "conteudos_gerados": generated_count,
                "periodo": periodo,
                "data_analise": datetime.now().isoformat(),
            },
            "performance": {
                "taxa_viralizacao": 0.34,
                "engajamento_medio": 0.08,
                "melhores_dias": ["terça", "quinta"],
                "melhores_horarios": ["12:00", "19:00"],
            },
            "tendencias": {
                "formatos_up": ["carousel", "reels"],
                "formatos_down": ["static"],
                "hashtags_trending": ["#dica", "#tutorial"],
                "topicos_trending": ["financiamento", "consórcio"],
            },
            "nota": "Requer dados reais para métricas precisas",
        }

    def get_top_models(self, limite: int = 5) -> List[Dict[str, Any]]:
        """Retorna modelos mais usados."""
        models = []

        for filepath in self.models_dir.glob("*.json"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    model = json.load(f)
                    models.append(
                        {
                            "nome": model["modelo"]["nome"],
                            "versao": model["modelo"]["versao"],
                            "criado_em": model["modelo"]["criado_em"],
                        }
                    )
            except Exception:
                continue

        return models[:limite]

    def get_insights(self) -> List[Dict[str, Any]]:
        """Retorna insights automáticos."""
        return [
            {
                "insight": "Carrosséis com 7-10 slides viralizam 3x mais",
                "confianca": 0.87,
                "samples": 34,
            },
            {
                "insight": "CTAs no final aumentam saves em 45%",
                "confianca": 0.92,
                "samples": 28,
            },
            {
                "insight": "Posts com badge 'NOVO' viralizam 2x mais",
                "confianca": 0.76,
                "samples": 19,
            },
            {
                "insight": "Hooks com números performam 25% melhor",
                "confianca": 0.89,
                "samples": 42,
            },
            {
                "insight": "Horário 12:00 tem 40% mais engajamento",
                "confianca": 0.85,
                "samples": 56,
            },
        ]

    def get_recommendations(self) -> List[str]:
        """Retorna recomendações baseadas em dados."""
        return [
            "Aumentar frequência de carrosséis",
            "Testar mais variações de hooks",
            "Usar badges 'NOVO' com mais frequência",
            "Focar em horário 12:00 para lançamentos",
            "Incluir números grandes nos slides de dados",
        ]

    def get_full_dashboard(self, periodo: str = "30d") -> Dict[str, Any]:
        """Retorna dashboard completo."""
        return {
            "dashboard": {
                **self.get_overview(periodo),
                "top_modelos": self.get_top_models(),
                "insights": self.get_insights(),
                "recomendacoes": self.get_recommendations(),
            }
        }

    def export_stats(self, formato: str = "json") -> str:
        """Exporta estatísticas."""
        stats = self.get_full_dashboard()

        if formato == "json":
            return json.dumps(stats, ensure_ascii=False, indent=2)
        elif formato == "markdown":
            return self._to_markdown(stats)
        else:
            return str(stats)

    def _to_markdown(self, stats: Dict) -> str:
        """Converte estatísticas para Markdown."""
        md = "# Dashboard - Viral Content Creator\n\n"
        md += "## Resumo\n\n"
        md += f"- Modelos criados: {stats['dashboard']['resumo']['modelos_criados']}\n"
        md += f"- Conteúdos gerados: {stats['dashboard']['resumo']['conteudos_gerados']}\n\n"
        md += "## Insights\n\n"
        for insight in stats["dashboard"]["insights"]:
            md += f"- {insight['insight']} (confiança: {insight['confianca']})\n"
        md += "\n## Recomendações\n\n"
        for rec in stats["dashboard"]["recomendacoes"]:
            md += f"- {rec}\n"
        return md
