"""
Analytics Module - Neuro Skills Agent
Autor: Monrars (@monrars)

Sistema de análise de performance e insights.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import json
from pathlib import Path


class AnalyticsEngine:
    """Motor de análise de performance."""

    def __init__(self, api_client, memory_manager):
        self.api = api_client
        self.memory = memory_manager

        # Diretório para análises
        self.analytics_dir = Path.home() / ".neuro-skills" / "analytics"
        self.analytics_dir.mkdir(parents=True, exist_ok=True)

    # ==================== PERFORMANCE ANALYSIS ====================

    def analyze_account(
        self, date_range: str = "last_7d", breakdown: str = "campaign"
    ) -> Dict:
        """
        Análise completa da conta.

        Args:
            date_range: Período de análise
            breakdown: Agrupamento (campaign, adset, ad, day)

        Returns:
            Dict com análise completa
        """
        # Obter insights gerais
        account_insights = self.api.get_ad_account_insights(date_range)

        # Obter insights por breakdown
        if breakdown != "account":
            breakdown_insights = self.api.get_insights(
                object_id=self.api.ad_account_id,
                level=breakdown,
                date_range=date_range,
                breakdowns=[breakdown],
            )
        else:
            breakdown_insights = None

        # Calcular métricas
        metrics = self._calculate_metrics(account_insights, breakdown_insights)

        # Identificar tendências
        trends = self._identify_trends(account_insights)

        # Gerar insights
        insights = self._generate_insights(metrics, trends)

        # Identificar oportunidades
        opportunities = self._identify_opportunities(metrics, trends)

        # Identificar problemas
        problems = self._identify_problems(metrics, trends)

        # Gerar recomendações
        recommendations = self._generate_recommendations(metrics, trends, problems)

        return {
            "timestamp": datetime.now().isoformat(),
            "date_range": date_range,
            "breakdown": breakdown,
            "metrics": metrics,
            "trends": trends,
            "insights": insights,
            "opportunities": opportunities,
            "problems": problems,
            "recommendations": recommendations,
            "account_insights": account_insights,
            "breakdown_insights": breakdown_insights,
        }

    def analyze_campaign(
        self,
        campaign_id: str,
        date_range: str = "last_7d",
        include_adsets: bool = True,
        include_ads: bool = True,
    ) -> Dict:
        """
        Análise detalhada de uma campanha.

        Args:
            campaign_id: ID da campanha
            date_range: Período de análise
            include_adsets: Incluir análise de ad sets
            include_ads: Incluir análise de ads

        Returns:
            Dict com análise da campanha
        """
        # Obter insights da campanha
        campaign_insights = self.api.get_campaign_insights(
            campaign_id=campaign_id, date_range=date_range
        )

        # Obter detalhes da campanha
        campaign_details = self.api.get_campaign(campaign_id)

        # Calcular métricas
        metrics = self._calculate_metrics(campaign_insights, None)

        # Performance por dia
        daily_performance = self._get_daily_performance(campaign_id, date_range)

        # Performance por ad set
        adset_performance = []
        if include_adsets:
            adsets = self.api.list_adsets(campaign_id)
            for adset in adsets.get("adsets", []):
                adset_insights = self.api.get_adset_insights(
                    adset_id=adset["id"], date_range=date_range
                )
                adset_performance.append(
                    {
                        "id": adset["id"],
                        "name": adset["name"],
                        "insights": adset_insights,
                    }
                )

        # Performance por ad
        ad_performance = []
        if include_ads:
            for adset in adsets.get("adsets", []):
                ads = self.api.list_ads(adset["id"])
                for ad in ads.get("ads", []):
                    ad_insights = self.api.get_ad_insights(
                        ad_id=ad["id"], date_range=date_range
                    )
                    ad_performance.append(
                        {
                            "id": ad["id"],
                            "name": ad["name"],
                            "adset_id": adset["id"],
                            "insights": ad_insights,
                        }
                    )

        # Análise de criativos
        creative_analysis = self._analyze_creatives(ad_performance)

        # Identificar best performers
        best_performers = self._identify_best_performers(ad_performance)

        # Identificar worst performers
        worst_performers = self._identify_worst_performers(ad_performance)

        # Gerar recomendações
        recommendations = self._generate_campaign_recommendations(
            metrics, daily_performance, best_performers, worst_performers
        )

        return {
            "timestamp": datetime.now().isoformat(),
            "campaign_id": campaign_id,
            "campaign_name": campaign_details.get("name"),
            "date_range": date_range,
            "metrics": metrics,
            "daily_performance": daily_performance,
            "adset_performance": adset_performance,
            "ad_performance": ad_performance,
            "creative_analysis": creative_analysis,
            "best_performers": best_performers,
            "worst_performers": worst_performers,
            "recommendations": recommendations,
        }

    def compare_periods(
        self, campaign_id: str, period1: str = "last_7d", period2: str = "previous_7d"
    ) -> Dict:
        """
        Compara performance entre dois períodos.

        Args:
            campaign_id: ID da campanha
            period1: Primeiro período
            period2: Segundo período

        Returns:
            Dict com comparação
        """
        # Obter insights dos dois períodos
        insights1 = self.api.get_campaign_insights(campaign_id, period1)
        insights2 = self.api.get_campaign_insights(campaign_id, period2)

        # Calcular métricas
        metrics1 = self._calculate_metrics(insights1, None)
        metrics2 = self._calculate_metrics(insights2, None)

        # Calcular variações
        variations = {}
        for key in metrics1:
            if key in metrics2:
                val1 = metrics1[key]
                val2 = metrics2[key]

                if val2 != 0:
                    variation = ((val1 - val2) / val2) * 100
                else:
                    variation = 100 if val1 > 0 else 0

                variations[key] = {
                    "current": val1,
                    "previous": val2,
                    "variation": variation,
                    "variation_abs": val1 - val2,
                }

        # Identificar melhorias e pioras
        improvements = []
        declines = []

        for key, var in variations.items():
            # Para métricas negativas (CPA), decréscimo é melhora
            if key in ["cpa", "cpc", "cpm"]:
                if var["variation"] < 0:
                    improvements.append((key, var))
                elif var["variation"] > 0:
                    declines.append((key, var))
            else:
                # Para métricas positivas (ROAS, CTR), aumento é melhora
                if var["variation"] > 0:
                    improvements.append((key, var))
                elif var["variation"] < 0:
                    declines.append((key, var))

        # Gerar insights
        insights = []

        if improvements:
            for metric, var in improvements[:3]:
                insights.append(
                    {
                        "type": "improvement",
                        "metric": metric,
                        "message": f"{metric} melhorou {abs(var['variation']):.1f}% ({var['previous']:.2f} → {var['current']:.2f})",
                        "importance": "high"
                        if abs(var["variation"]) > 20
                        else "medium",
                    }
                )

        if declines:
            for metric, var in declines[:3]:
                insights.append(
                    {
                        "type": "decline",
                        "metric": metric,
                        "message": f"{metric} piorou {abs(var['variation']):.1f}% ({var['previous']:.2f} → {var['current']:.2f})",
                        "importance": "high"
                        if abs(var["variation"]) > 20
                        else "medium",
                    }
                )

        return {
            "timestamp": datetime.now().isoformat(),
            "period1": period1,
            "period2": period2,
            "metrics_current": metrics1,
            "metrics_previous": metrics2,
            "variations": variations,
            "improvements": improvements,
            "declines": declines,
            "insights": insights,
        }

    # ==================== HELPER METHODS ====================

    def _calculate_metrics(
        self, insights: Dict, breakdown_insights: Optional[Dict]
    ) -> Dict:
        """Calcula métricas derivadas."""
        metrics = {}

        # Métricas básicas
        metrics["spend"] = float(insights.get("spend", 0))
        metrics["impressions"] = int(insights.get("impressions", 0))
        metrics["clicks"] = int(insights.get("clicks", 0))
        metrics["reach"] = int(insights.get("reach", 0))

        # Métricas calculadas
        if metrics["impressions"] > 0:
            metrics["ctr"] = (metrics["clicks"] / metrics["impressions"]) * 100
            metrics["cpm"] = (metrics["spend"] / metrics["impressions"]) * 1000

        if metrics["clicks"] > 0:
            metrics["cpc"] = metrics["spend"] / metrics["clicks"]

        # Ações
        actions = insights.get("actions", [])
        for action in actions:
            metrics[f"action_{action['action_type']}"] = int(action["value"])

        # CPA
        cost_per_action = insights.get("cost_per_action_type", [])
        for cpa in cost_per_action:
            metrics[f"cpa_{cpa['action_type']}"] = float(cpa["value"])

        # ROAS (se tiver purchases)
        if "action_purchase" in metrics and metrics["action_purchase"] > 0:
            # Assumindo valor médio de compra (deveria vir de pixel)
            metrics["roas"] = metrics["action_purchase"] / metrics["spend"]

        # Frequência
        if metrics["reach"] > 0:
            metrics["frequency"] = metrics["impressions"] / metrics["reach"]

        return metrics

    def _identify_trends(self, insights: Dict) -> Dict:
        """Identifica tendências."""
        # Implementar análise de tendências
        # Por enquanto retorna básico
        return {
            "spend_trend": "stable",
            "cpa_trend": "stable",
            "roas_trend": "stable",
            "confidence": 0.7,
        }

    def _generate_insights(self, metrics: Dict, trends: Dict) -> List[Dict]:
        """Gera insights."""
        insights = []

        # CPA
        cpa = metrics.get("cpa_purchase", metrics.get("cpa", 0))
        if cpa > 0:
            if cpa > 100:
                insights.append(
                    {
                        "type": "warning",
                        "category": "cpa",
                        "message": f"CPA está alto em R${cpa:.2f}",
                        "recommendation": "Considere pausar criativos com pior performance",
                    }
                )
            elif cpa < 30:
                insights.append(
                    {
                        "type": "success",
                        "category": "cpa",
                        "message": f"CPA excelente em R${cpa:.2f}",
                        "recommendation": "Considere aumentar orçamento",
                    }
                )

        # ROAS
        roas = metrics.get("roas", 0)
        if roas > 0:
            if roas > 3:
                insights.append(
                    {
                        "type": "success",
                        "category": "roas",
                        "message": f"ROAS excelente em {roas:.2f}x",
                        "recommendation": "Escala a campanha",
                    }
                )
            elif roas < 1.5:
                insights.append(
                    {
                        "type": "warning",
                        "category": "roas",
                        "message": f"ROAS baixo em {roas:.2f}x",
                        "recommendation": "Teste novos criativos",
                    }
                )

        # CTR
        ctr = metrics.get("ctr", 0)
        if ctr > 0:
            if ctr > 2:
                insights.append(
                    {
                        "type": "success",
                        "category": "ctr",
                        "message": f"CTR bom em {ctr:.2f}%",
                        "recommendation": "Criativos funcionam bem",
                    }
                )
            elif ctr < 0.5:
                insights.append(
                    {
                        "type": "warning",
                        "category": "ctr",
                        "message": f"CTR baixo em {ctr:.2f}%",
                        "recommendation": "Revise os criativos",
                    }
                )

        return insights

    def _identify_opportunities(self, metrics: Dict, trends: Dict) -> List[Dict]:
        """Identifica oportunidades."""
        opportunities = []

        # Se ROAS alto, oportunidade de escala
        if metrics.get("roas", 0) > 3:
            opportunities.append(
                {
                    "type": "scale",
                    "priority": "high",
                    "message": "ROAS alto indica oportunidade de escala",
                    "action": "Aumentar orçamento em 20-30%",
                }
            )

        # Se CPA baixo e CTR alto, oportunidade de expansão
        if metrics.get("cpa_purchase", 1000) < 30 and metrics.get("ctr", 0) > 2:
            opportunities.append(
                {
                    "type": "expand",
                    "priority": "medium",
                    "message": "Performance boa indica oportunidade de expandir público",
                    "action": "Testar novos públicos",
                }
            )

        return opportunities

    def _identify_problems(self, metrics: Dict, trends: Dict) -> List[Dict]:
        """Identifica problemas."""
        problems = []

        # CPA alto
        cpa = metrics.get("cpa_purchase", metrics.get("cpa", 0))
        if cpa > 100:
            problems.append(
                {
                    "type": "high_cpa",
                    "severity": "high",
                    "message": f"CPA muito alto: R${cpa:.2f}",
                    "action": "Pausar criativos ruins e testar novos",
                }
            )

        # CTR baixo
        ctr = metrics.get("ctr", 0)
        if ctr < 0.5:
            problems.append(
                {
                    "type": "low_ctr",
                    "severity": "medium",
                    "message": f"CTR baixo: {ctr:.2f}%",
                    "action": "Testar novos criativos e copy",
                }
            )

        # Frequência alta
        frequency = metrics.get("frequency", 0)
        if frequency > 3:
            problems.append(
                {
                    "type": "high_frequency",
                    "severity": "medium",
                    "message": f"Frequência alta: {frequency:.1f}",
                    "action": "Expandir público ou pausar temporariamente",
                }
            )

        return problems

    def _generate_recommendations(
        self, metrics: Dict, trends: Dict, problems: List[Dict]
    ) -> List[Dict]:
        """Gera recomendações."""
        recommendations = []

        # Recomendações baseadas em problemas
        for problem in problems:
            if problem["type"] == "high_cpa":
                recommendations.append(
                    {
                        "priority": "high",
                        "category": "optimization",
                        "action": "pause_low_performers",
                        "message": "Pausar criativos com CPA acima de R$100",
                        "params": {"threshold": 100},
                    }
                )

            elif problem["type"] == "low_ctr":
                recommendations.append(
                    {
                        "priority": "medium",
                        "category": "creative",
                        "action": "test_new_creatives",
                        "message": "Testar novos criativos com copy otimizado",
                        "params": {"num_variations": 3},
                    }
                )

            elif problem["type"] == "high_frequency":
                recommendations.append(
                    {
                        "priority": "medium",
                        "category": "audience",
                        "action": "expand_audience",
                        "message": "Expandir público ou usar lookalike",
                        "params": {"lookalike_size": 5},
                    }
                )

        # Recomendações baseadas em performance
        if metrics.get("roas", 0) > 3:
            recommendations.append(
                {
                    "priority": "high",
                    "category": "scale",
                    "action": "increase_budget",
                    "message": "Aumentar orçamento em 20%",
                    "params": {"factor": 1.2},
                }
            )

        return recommendations

    def _get_daily_performance(self, campaign_id: str, date_range: str) -> List[Dict]:
        """Obtém performance por dia."""
        # Implementar breakdown por dia
        # Por enquanto retorna lista vazia
        return []

    def _analyze_creatives(self, ad_performance: List[Dict]) -> Dict:
        """Analisa performance de criativos."""
        if not ad_performance:
            return {}

        # Ordenar por performance
        sorted_ads = sorted(
            ad_performance, key=lambda x: x["insights"].get("ctr", 0), reverse=True
        )

        return {
            "total_creatives": len(ad_performance),
            "best_performing": sorted_ads[:3] if len(sorted_ads) >= 3 else sorted_ads,
            "worst_performing": sorted_ads[-3:] if len(sorted_ads) >= 3 else [],
            "avg_ctr": sum(ad["insights"].get("ctr", 0) for ad in ad_performance)
            / len(ad_performance),
        }

    def _identify_best_performers(self, ad_performance: List[Dict]) -> List[Dict]:
        """Identifica melhores performers."""
        if not ad_performance:
            return []

        # Ordenar por ROAS ou CTR
        sorted_ads = sorted(
            ad_performance,
            key=lambda x: (
                x["insights"].get("purchase_roas", 0),
                x["insights"].get("ctr", 0),
            ),
            reverse=True,
        )

        return [
            {
                "id": ad["id"],
                "name": ad["name"],
                "roas": ad["insights"].get("purchase_roas", 0),
                "ctr": ad["insights"].get("ctr", 0),
                "cpa": ad["insights"]
                .get("cost_per_action_type", {})
                .get("purchase", 0),
            }
            for ad in sorted_ads[:5]
        ]

    def _identify_worst_performers(self, ad_performance: List[Dict]) -> List[Dict]:
        """Identifica piores performers."""
        if not ad_performance:
            return []

        # Ordenar por pior performance
        sorted_ads = sorted(
            ad_performance,
            key=lambda x: (
                x["insights"].get("purchase_roas", 0),
                x["insights"].get("ctr", 0),
            ),
        )

        return [
            {
                "id": ad["id"],
                "name": ad["name"],
                "roas": ad["insights"].get("purchase_roas", 0),
                "ctr": ad["insights"].get("ctr", 0),
                "cpa": ad["insights"]
                .get("cost_per_action_type", {})
                .get("purchase", 0),
            }
            for ad in sorted_ads[:5]
        ]

    def _generate_campaign_recommendations(
        self,
        metrics: Dict,
        daily_performance: List[Dict],
        best_performers: List[Dict],
        worst_performers: List[Dict],
    ) -> List[Dict]:
        """Gera recomendações para campanha."""
        recommendations = []

        # Se tem piores performers, recomendar pausa
        if worst_performers:
            recommendations.append(
                {
                    "priority": "high",
                    "action": "pause_worst_performers",
                    "message": f"Pausar {len(worst_performers)} criativos com baixa performance",
                    "details": [wp["id"] for wp in worst_performers],
                }
            )

        # Se tem best performers, recomendar escala
        if best_performers and metrics.get("roas", 0) > 2:
            recommendations.append(
                {
                    "priority": "high",
                    "action": "scale_best_performers",
                    "message": "Escalar criativos com boa performance",
                    "details": [bp["id"] for bp in best_performers[:2]],
                }
            )

        return recommendations

    # ==================== REPORTS ====================

    def generate_report(
        self,
        report_type: str = "performance",
        campaigns: List[str] = None,
        date_range: str = "last_7d",
        format: str = "json",
    ) -> Dict:
        """
        Gera relatório completo.

        Args:
            report_type: Tipo de relatório (performance, creative, audience)
            campaigns: Lista de campaign_ids (None = todas)
            date_range: Período
            format: Formato de saída (json, csv, excel)

        Returns:
            Dict com relatório
        """
        if report_type == "performance":
            return self._generate_performance_report(campaigns, date_range)
        elif report_type == "creative":
            return self._generate_creative_report(campaigns, date_range)
        elif report_type == "audience":
            return self._generate_audience_report(campaigns, date_range)

        return {}

    def _generate_performance_report(
        self, campaigns: List[str], date_range: str
    ) -> Dict:
        """Gera relatório de performance."""
        # Obter todas as campanhas se não especificado
        if not campaigns:
            all_campaigns = self.api.list_campaigns(status="ACTIVE")
            campaigns = [c["id"] for c in all_campaigns.get("campaigns", [])]

        # Coletar dados
        data = []
        for campaign_id in campaigns:
            try:
                analysis = self.analyze_campaign(campaign_id, date_range)
                data.append(analysis)
            except Exception as e:
                data.append({"campaign_id": campaign_id, "error": str(e)})

        # Calcular totais
        totals = self._calculate_totals(data)

        # Gerar resumo executivo
        summary = self._generate_executive_summary(data, totals)

        return {
            "report_type": "performance",
            "date_range": date_range,
            "timestamp": datetime.now().isoformat(),
            "summary": summary,
            "totals": totals,
            "campaigns": data,
        }

    def _generate_creative_report(self, campaigns: List[str], date_range: str) -> Dict:
        """Gera relatório de criativos."""
        # Implementar
        return {}

    def _generate_audience_report(self, campaigns: List[str], date_range: str) -> Dict:
        """Gera relatório de públicos."""
        # Implementar
        return {}

    def _calculate_totals(self, data: List[Dict]) -> Dict:
        """Calcula totais do relatório."""
        totals = {
            "spend": 0,
            "impressions": 0,
            "clicks": 0,
            "conversions": 0,
            "cpa": 0,
            "roas": 0,
        }

        valid_data = [d for d in data if "error" not in d]

        if not valid_data:
            return totals

        for item in valid_data:
            metrics = item.get("metrics", {})
            totals["spend"] += metrics.get("spend", 0)
            totals["impressions"] += metrics.get("impressions", 0)
            totals["clicks"] += metrics.get("clicks", 0)
            totals["conversions"] += metrics.get("action_purchase", 0)

        # Calcular métricas médias
        if totals["clicks"] > 0:
            totals["cpa"] = totals["spend"] / totals["clicks"]

        if totals["conversions"] > 0:
            totals["roas"] = totals["conversions"] / totals["spend"]

        return totals

    def _generate_executive_summary(self, data: List[Dict], totals: Dict) -> Dict:
        """Gera resumo executivo."""
        valid_data = [d for d in data if "error" not in d]

        return {
            "total_campaigns": len(data),
            "active_campaigns": len(valid_data),
            "total_spend": totals["spend"],
            "total_conversions": totals["conversions"],
            "average_roas": totals["roas"],
            "average_cpa": totals["cpa"],
            "best_performing": max(
                valid_data,
                key=lambda x: x.get("metrics", {}).get("roas", 0),
                default={},
            ),
            "worst_performing": min(
                valid_data,
                key=lambda x: x.get("metrics", {}).get("roas", float("inf")),
                default={},
            ),
        }
