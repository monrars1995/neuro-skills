"""
Scheduler Module - Neuro Skills Agent
Autor: Monrars (@monrars)

Sistema de agendamento para automações e análises.
"""

import schedule
import time
import threading
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path


class AutomationScheduler:
    """Agendador de automações com suporte a crons."""

    def __init__(self, memory_manager, api_client):
        self.memory = memory_manager
        self.api_client = api_client
        self.jobs = []
        self.running = False
        self.thread = None

        # Diretório para salvar jobs
        self.jobs_dir = Path.home() / ".neuro-skills" / "scheduler"
        self.jobs_dir.mkdir(parents=True, exist_ok=True)

        # Carregar jobs salvos
        self._load_jobs()

    # ==================== JOB MANAGEMENT ====================

    def add_job(
        self,
        job_id: str,
        job_type: str,
        schedule_type: str,
        schedule_value: str,
        params: Dict = None,
        enabled: bool = True,
    ) -> Dict:
        """
        Adiciona um job agendado.

        Args:
            job_id: ID único do job
            job_type: Tipo do job (analysis, optimization, report, rule)
            schedule_type: Tipo de agendamento (interval, daily, weekly, monthly)
            schedule_value: Valor do agendamento (ex: "09:00", "1h", "monday")
            params: Parâmetros do job
            enabled: Se está ativo

        Returns:
            Dict com job criado
        """
        job = {
            "id": job_id,
            "type": job_type,
            "schedule_type": schedule_type,
            "schedule_value": schedule_value,
            "params": params or {},
            "enabled": enabled,
            "created_at": datetime.now().isoformat(),
            "last_run": None,
            "next_run": None,
            "run_count": 0,
            "last_result": None,
        }

        self.jobs.append(job)
        self._save_jobs()

        return job

    def remove_job(self, job_id: str) -> bool:
        """Remove um job."""
        for i, job in enumerate(self.jobs):
            if job["id"] == job_id:
                self.jobs.pop(i)
                self._save_jobs()
                return True
        return False

    def toggle_job(self, job_id: str) -> Optional[Dict]:
        """Ativa/desativa um job."""
        for job in self.jobs:
            if job["id"] == job_id:
                job["enabled"] = not job["enabled"]
                self._save_jobs()
                return job
        return None

    def get_jobs(self, job_type: str = None) -> List[Dict]:
        """Lista jobs."""
        if job_type:
            return [j for j in self.jobs if j["type"] == job_type]
        return self.jobs

    def get_job(self, job_id: str) -> Optional[Dict]:
        """Obtém um job específico."""
        for job in self.jobs:
            if job["id"] == job_id:
                return job
        return None

    # ==================== SCHEDULING ====================

    def start(self):
        """Inicia o scheduler em background."""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()

    def stop(self):
        """Para o scheduler."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)

    def _run_scheduler(self):
        """Loop principal do scheduler."""
        while self.running:
            self._check_jobs()
            time.sleep(60)  # Checa a cada minuto

    def _check_jobs(self):
        """Verifica e executa jobs agendados."""
        now = datetime.now()

        for job in self.jobs:
            if not job["enabled"]:
                continue

            if self._should_run(job, now):
                self._execute_job(job)

    def _should_run(self, job: Dict, now: datetime) -> bool:
        """Verifica se o job deve rodar."""
        schedule_type = job["schedule_type"]
        schedule_value = job["schedule_value"]
        last_run = job.get("last_run")

        if last_run:
            last_run_dt = datetime.fromisoformat(last_run)
        else:
            last_run_dt = None

        if schedule_type == "interval":
            # Ex: "1h", "30m", "24h"
            interval = self._parse_interval(schedule_value)
            if last_run_dt:
                return (now - last_run_dt) >= timedelta(seconds=interval)
            return True

        elif schedule_type == "daily":
            # Ex: "09:00"
            target_time = datetime.strptime(schedule_value, "%H:%M").time()
            now_time = now.time()

            # Se já passou da hora hoje e ainda não rodou
            if now_time >= target_time:
                if not last_run_dt or last_run_dt.date() < now.date():
                    return True
            return False

        elif schedule_type == "weekly":
            # Ex: "monday 09:00"
            parts = schedule_value.split()
            day_name = parts[0].lower()
            hour = parts[1] if len(parts) > 1 else "09:00"

            days = {
                "monday": 0,
                "tuesday": 1,
                "wednesday": 2,
                "thursday": 3,
                "friday": 4,
                "saturday": 5,
                "sunday": 6,
            }

            target_day = days.get(day_name, 0)
            target_time = datetime.strptime(hour, "%H:%M").time()

            if now.weekday() == target_day and now.time() >= target_time:
                if not last_run_dt or last_run_dt.date() < now.date():
                    return True
            return False

        elif schedule_type == "monthly":
            # Ex: "01 09:00" (dia 1 às 09:00)
            parts = schedule_value.split()
            day = int(parts[0])
            hour = parts[1] if len(parts) > 1 else "09:00"

            target_time = datetime.strptime(hour, "%H:%M").time()

            if now.day == day and now.time() >= target_time:
                if not last_run_dt or last_run_dt.month < now.month:
                    return True
            return False

        return False

    def _parse_interval(self, value: str) -> int:
        """Parse interval string to seconds."""
        if value.endswith("m"):
            return int(value[:-1]) * 60
        elif value.endswith("h"):
            return int(value[:-1]) * 3600
        elif value.endswith("d"):
            return int(value[:-1]) * 86400
        return int(value)

    # ==================== EXECUTION ====================

    def _execute_job(self, job: Dict) -> Dict:
        """Executa um job."""
        job_type = job["type"]
        params = job.get("params", {})

        try:
            if job_type == "analysis":
                result = self._run_analysis(params)
            elif job_type == "optimization":
                result = self._run_optimization(params)
            elif job_type == "report":
                result = self._run_report(params)
            elif job_type == "rule":
                result = self._run_rule(params)
            else:
                result = {"error": f"Unknown job type: {job_type}"}
        except Exception as e:
            result = {"error": str(e)}

        # Atualizar job
        job["last_run"] = datetime.now().isoformat()
        job["run_count"] += 1
        job["last_result"] = result
        self._save_jobs()

        return result

    def _run_analysis(self, params: Dict) -> Dict:
        """Executa análise de performance."""
        client_id = params.get("client_id")
        campaigns = params.get("campaigns", [])
        metrics = params.get("metrics", ["spend", "clicks", "cpa", "roas"])

        results = {
            "timestamp": datetime.now().isoformat(),
            "client_id": client_id,
            "campaigns": [],
            "alerts": [],
            "recommendations": [],
        }

        try:
            # Obter insights de cada campanha
            for campaign_id in campaigns:
                insights = self.api_client.get_campaign_insights(
                    campaign_id=campaign_id, date_range="last_7d"
                )

                if "error" not in insights:
                    results["campaigns"].append(
                        {"campaign_id": campaign_id, "insights": insights}
                    )

                    # Gerar alertas
                    alerts = self._generate_alerts(insights, params)
                    results["alerts"].extend(alerts)

            # Gerar recomendações
            results["recommendations"] = self._generate_recommendations(results)

            # Salvar na memória
            if client_id:
                self.memory.save_analysis(client_id, results)

        except Exception as e:
            results["error"] = str(e)

        return results

    def _run_optimization(self, params: Dict) -> Dict:
        """Executa otimização automática."""
        client_id = params.get("client_id")
        campaigns = params.get("campaigns", [])
        rules = params.get("rules", [])

        results = {
            "timestamp": datetime.now().isoformat(),
            "client_id": client_id,
            "optimizations": [],
            "errors": [],
        }

        for rule in rules:
            try:
                rule_type = rule.get("type")

                if rule_type == "scale_high_performers":
                    # Escalar campanhas com ROAS alto
                    scaling_results = self._scale_high_performers(campaigns, rule)
                    results["optimizations"].append(scaling_results)

                elif rule_type == "pause_low_performers":
                    # Pausar campanhas com CPA alto
                    pause_results = self._pause_low_performers(campaigns, rule)
                    results["optimizations"].append(pause_results)

                elif rule_type == "budget_reallocation":
                    # Realocar orçamento
                    realloc_results = self._reallocate_budget(campaigns, rule)
                    results["optimizations"].append(realloc_results)

                elif rule_type == "creative_rotation":
                    # Rotacionar criativos
                    rotation_results = self._rotate_creatives(campaigns, rule)
                    results["optimizations"].append(rotation_results)

            except Exception as e:
                results["errors"].append({"rule": rule_type, "error": str(e)})

        # Salvar na memória
        if client_id:
            self.memory.save_optimization(client_id, results)

        return results

    def _run_report(self, params: Dict) -> Dict:
        """Gera relatório."""
        client_id = params.get("client_id")
        report_type = params.get("report_type", "performance")
        date_range = params.get("date_range", "last_7d")
        format_type = params.get("format", "json")
        email = params.get("email")

        # Gerar relatório
        report = self.api_client.generate_report(
            report_type=report_type, date_range=date_range
        )

        # Formatar
        if format_type == "csv":
            report["formatted"] = self._format_csv(report)
        elif format_type == "excel":
            report["formatted"] = self._format_excel(report)

        # Enviar por email se especificado
        if email:
            self._send_email_report(email, report)

        return report

    def _run_rule(self, params: Dict) -> Dict:
        """Executa regras de automação."""
        rule_id = params.get("rule_id")

        # Executar regra específica
        return self.api_client.execute_rules([rule_id])

    # ==================== OPTIMIZATION HELPERS ====================

    def _scale_high_performers(self, campaigns: List[str], rule: Dict) -> Dict:
        """Escala campanhas com alta performance."""
        threshold = rule.get("roas_threshold", 3.0)
        scale_factor = rule.get("scale_factor", 1.2)

        results = {"scaled": [], "skipped": []}

        for campaign_id in campaigns:
            insights = self.api_client.get_campaign_insights(
                campaign_id=campaign_id, date_range="last_3d"
            )

            roas = insights.get("purchase_roas", 0)

            if roas > threshold:
                # Obter orçamento atual
                campaign = self.api_client.get_campaign(campaign_id)
                current_budget = campaign.get("daily_budget", 0)
                new_budget = int(current_budget * scale_factor)

                # Atualizar
                self.api_client.update_campaign(
                    campaign_id=campaign_id, budget=new_budget
                )

                results["scaled"].append(
                    {
                        "campaign_id": campaign_id,
                        "old_budget": current_budget,
                        "new_budget": new_budget,
                        "roas": roas,
                    }
                )
            else:
                results["skipped"].append({"campaign_id": campaign_id, "roas": roas})

        return results

    def _pause_low_performers(self, campaigns: List[str], rule: Dict) -> Dict:
        """Pausa campanhas com baixa performance."""
        threshold = rule.get("cpa_threshold", 100)
        min_spend = rule.get("min_spend", 50)

        results = {"paused": [], "kept": []}

        for campaign_id in campaigns:
            insights = self.api_client.get_campaign_insights(
                campaign_id=campaign_id, date_range="last_7d"
            )

            spend = float(insights.get("spend", 0))
            cpa = insights.get("cost_per_action_type", {}).get("purchase", 0)

            if spend >= min_spend and cpa > threshold:
                # Pausar
                self.api_client.update_campaign(
                    campaign_id=campaign_id, status="PAUSED"
                )

                results["paused"].append(
                    {"campaign_id": campaign_id, "cpa": cpa, "spend": spend}
                )
            else:
                results["kept"].append(
                    {"campaign_id": campaign_id, "cpa": cpa, "spend": spend}
                )

        return results

    def _reallocate_budget(self, campaigns: List[str], rule: Dict) -> Dict:
        """Realoca orçamento entre campanhas."""
        total_budget = rule.get("total_budget")
        allocation_method = rule.get("method", "performance_based")

        results = {"reallocated": []}

        # Obter performance de todas as campanhas
        performances = []
        for campaign_id in campaigns:
            insights = self.api_client.get_campaign_insights(
                campaign_id=campaign_id, date_range="last_7d"
            )
            performances.append(
                {
                    "campaign_id": campaign_id,
                    "roas": insights.get("purchase_roas", 0),
                    "cpa": insights.get("cost_per_action_type", {}).get("purchase", 0),
                }
            )

        # Calcular novos orçamentos
        if allocation_method == "performance_based":
            # Alocar proporcionalmente ao ROAS
            total_roas = sum(p["roas"] for p in performances if p["roas"] > 0)

            for p in performances:
                if total_roas > 0 and p["roas"] > 0:
                    share = p["roas"] / total_roas
                    new_budget = int(total_budget * share)

                    self.api_client.update_campaign(
                        campaign_id=p["campaign_id"], budget=new_budget
                    )

                    results["reallocated"].append(
                        {
                            "campaign_id": p["campaign_id"],
                            "new_budget": new_budget,
                            "roas": p["roas"],
                        }
                    )

        return results

    def _rotate_creatives(self, campaigns: List[str], rule: Dict) -> Dict:
        """Rotaciona criativos com base na performance."""
        results = {"rotated": [], "unchanged": []}

        for campaign_id in campaigns:
            # Obter ads da campanha
            adsets = self.api_client.list_adsets(campaign_id)

            for adset in adsets.get("adsets", []):
                ads = self.api_client.list_ads(adset["id"])

                # Ordenar por performance
                sorted_ads = sorted(
                    ads.get("ads", []), key=lambda x: x.get("ctr", 0), reverse=True
                )

                # Pausar os piores
                if len(sorted_ads) > 3:
                    for ad in sorted_ads[3:]:
                        self.api_client.update_ad(ad_id=ad["id"], status="PAUSED")

                        results["rotated"].append(
                            {"ad_id": ad["id"], "ctr": ad.get("ctr", 0)}
                        )

        return results

    # ==================== ALERTS & RECOMMENDATIONS ====================

    def _generate_alerts(self, insights: Dict, params: Dict) -> List[Dict]:
        """Gera alertas baseado nos insights."""
        alerts = []

        # Alerta de CPA alto
        cpa_threshold = params.get("cpa_threshold", 100)
        cpa = insights.get("cost_per_action_type", {}).get("purchase", 0)
        if cpa > cpa_threshold:
            alerts.append(
                {
                    "type": "high_cpa",
                    "level": "warning",
                    "message": f"CPA alto: R${cpa:.2f}",
                    "value": cpa,
                    "threshold": cpa_threshold,
                }
            )

        # Alerta de ROAS baixo
        roas_threshold = params.get("roas_threshold", 2.0)
        roas = insights.get("purchase_roas", 0)
        if roas < roas_threshold and roas > 0:
            alerts.append(
                {
                    "type": "low_roas",
                    "level": "critical",
                    "message": f"ROAS baixo: {roas:.2f}x",
                    "value": roas,
                    "threshold": roas_threshold,
                }
            )

        # Alerta de CTR baixo
        ctr_threshold = params.get("ctr_threshold", 1.0)
        ctr = insights.get("ctr", 0)
        if ctr < ctr_threshold:
            alerts.append(
                {
                    "type": "low_ctr",
                    "level": "warning",
                    "message": f"CTR baixo: {ctr:.2f}%",
                    "value": ctr,
                    "threshold": ctr_threshold,
                }
            )

        # Alerta de spend alto
        spend_threshold = params.get("spend_threshold", 1000)
        spend = float(insights.get("spend", 0))
        if spend > spend_threshold:
            alerts.append(
                {
                    "type": "high_spend",
                    "level": "info",
                    "message": f"Gasto alto: R${spend:.2f}",
                    "value": spend,
                    "threshold": spend_threshold,
                }
            )

        return alerts

    def _generate_recommendations(self, results: Dict) -> List[Dict]:
        """Gera recomendações baseado na análise."""
        recommendations = []

        campaigns = results.get("campaigns", [])

        if not campaigns:
            return recommendations

        # Calcular médias
        total_spend = sum(float(c["insights"].get("spend", 0)) for c in campaigns)
        avg_cpa = (
            sum(
                c["insights"].get("cost_per_action_type", {}).get("purchase", 0)
                for c in campaigns
            )
            / len(campaigns)
            if campaigns
            else 0
        )

        avg_roas = (
            sum(c["insights"].get("purchase_roas", 0) for c in campaigns)
            / len(campaigns)
            if campaigns
            else 0
        )

        # Recomendação de escala
        if avg_roas > 3:
            recommendations.append(
                {
                    "type": "scale",
                    "priority": "high",
                    "message": f"ROAS médio de {avg_roas:.2f}x - Considere escalar campanhas",
                    "action": "increase_budget",
                    "params": {"factor": 1.2},
                }
            )

        # Recomendação de pausa
        if avg_cpa > 50:
            recommendations.append(
                {
                    "type": "pause",
                    "priority": "critical",
                    "message": f"CPA médio de R${avg_cpa:.2f} - Considere pausar criativos ruins",
                    "action": "pause_low_performers",
                    "params": {"cpa_threshold": avg_cpa * 1.5},
                }
            )

        # Recomendação de new creative
        if avg_roas < 2:
            recommendations.append(
                {
                    "type": "creative",
                    "priority": "high",
                    "message": "ROAS baixo - Teste novos criativos",
                    "action": "create_new_creative",
                    "params": {},
                }
            )

        return results

    # ==================== PERSISTENCE ====================

    def _load_jobs(self):
        """Carrega jobs salvos."""
        jobs_file = self.jobs_dir / "jobs.json"

        if jobs_file.exists():
            try:
                with open(jobs_file) as f:
                    self.jobs = json.load(f)
            except Exception:
                self.jobs = []

    def _save_jobs(self):
        """Salva jobs."""
        jobs_file = self.jobs_dir / "jobs.json"

        with open(jobs_file, "w") as f:
            json.dump(self.jobs, f, indent=2)

    # ==================== FORMATTERS ====================

    def _format_csv(self, report: Dict) -> str:
        """Formata relatório como CSV."""
        lines = []

        # Header
        lines.append("Campaign,CPA,ROAS,Spend,Clicks,CTR")

        # Data
        for campaign in report.get("details", []):
            lines.append(
                f"{campaign['name']},"
                f"{campaign.get('cpa', 0):.2f},"
                f"{campaign.get('roas', 0):.2f},"
                f"{campaign.get('spend', 0):.2f},"
                f"{campaign.get('clicks', 0)},"
                f"{campaign.get('ctr', 0):.2f}%"
            )

        return "\n".join(lines)

    def _format_excel(self, report: Dict) -> str:
        """Formata relatório para Excel."""
        # Implementar com openpyxl se necessário
        return self._format_csv(report)

    def _send_email_report(self, email: str, report: Dict):
        """Envia relatório por email."""
        # Implementar envio de email
        pass
