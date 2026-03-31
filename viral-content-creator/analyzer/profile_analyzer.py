"""Profile analyzer with real API delegation and safe fallbacks."""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.instagram_api import InstagramAPI
from api.tiktok_api import TikTokAPI
from api.twitter_api import TwitterAPI


class ProfileAnalyzer:
    PLATFORM_PATTERNS = {
        "instagram": r"(@[\w.]+|instagram\.com/[\w.]+)",
        "tiktok": r"(@[\w.]+|tiktok\.com/@[\w.]+)",
        "twitter": r"(@[\w.]+|twitter\.com/[\w.]+|x\.com/[\w.]+)",
        "linkedin": r"(in/[\w.-]+|linkedin\.com/in/[\w.-]+)",
        "youtube": r"(@[\w.]+|youtube\.com/@[\w.]+|youtube\.com/c/[\w.]+)",
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.cache: Dict[str, Dict[str, Any]] = {}
        self._instagram = InstagramAPI()
        self._tiktok = TikTokAPI()
        self._twitter = TwitterAPI()

    def analyze(
        self, username: str, plataforma: str, options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        options = options or {}
        username_clean = self._extract_username(username, plataforma)
        if not username_clean:
            return {"error": f"Username inválido para {plataforma}"}

        platform_result = self._fetch_platform_profile(
            username_clean, plataforma, options
        )
        if "perfil" in platform_result:
            platform_result["perfil"].setdefault(
                "data_analise", datetime.now().isoformat()
            )
            self.cache[username_clean] = platform_result
            return platform_result

        result = {
            "perfil": {
                "username": username_clean,
                "plataforma": plataforma,
                "data_analise": datetime.now().isoformat(),
                "metricas": self._default_metrics(),
                "frequencia_postagem": self._default_frequency(),
                "conteudo_analise": self._default_content_analysis(),
                "visual_pattern": self._default_visual_pattern(),
                "viralidade_score": self._default_virality_score(),
                "nota": platform_result.get(
                    "error", "Plataforma sem integração implementada."
                ),
            }
        }
        self.cache[username_clean] = result
        return result

    def analyze_batch(
        self,
        usernames: List[str],
        plataforma: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return {
            username: self.analyze(username, plataforma, options)
            for username in usernames
        }

    def get_insights(self, username: str) -> Dict[str, Any]:
        if username not in self.cache:
            return {"error": "Perfil não analisado ainda"}
        profile = self.cache[username]
        score = profile["perfil"]["viralidade_score"].get("score_geral", 0)
        insights = []
        if score >= 8.0:
            insights.append("Perfil com alto potencial de viralização")
        elif score >= 6.0:
            insights.append("Perfil com potencial moderado")
        else:
            insights.append("Perfil necessita otimizações")
        return {
            "username": username,
            "insights": insights,
            "recomendacoes": profile["perfil"]["viralidade_score"].get(
                "recomendacoes", []
            ),
        }

    def _fetch_platform_profile(
        self, username: str, plataforma: str, options: Dict[str, Any]
    ) -> Dict[str, Any]:
        if plataforma == "instagram":
            return self._instagram.analyze_profile(username, options)
        if plataforma == "tiktok":
            return self._tiktok.analyze_profile(username, options)
        if plataforma == "twitter":
            return self._twitter.analyze_profile(username, options)
        return {"error": f"Integração real ainda não disponível para {plataforma}"}

    def _extract_username(self, username: str, plataforma: str) -> Optional[str]:
        pattern = self.PLATFORM_PATTERNS.get(plataforma)
        if not pattern:
            return None
        match = re.search(pattern, username)
        if match:
            return match.group(1).replace("@", "").replace("in/", "")
        return username[1:] if username.startswith("@") else username

    def _default_metrics(self) -> Dict[str, Any]:
        return {
            "seguidores": 0,
            "seguindo": 0,
            "posts_total": 0,
            "engajamento_medio": 0.0,
            "alcance_estimado": 0,
        }

    def _default_frequency(self) -> Dict[str, Any]:
        return {
            "posts_semana": 0,
            "melhores_dias": ["terça", "quinta", "sábado"],
            "melhores_horarios": ["12:00", "19:00", "21:00"],
        }

    def _default_content_analysis(self) -> Dict[str, Any]:
        return {
            "tipos": {
                "carousel": {"quantidade": 0, "engajamento": 0.0},
                "reels": {"quantidade": 0, "engajamento": 0.0},
                "static": {"quantidade": 0, "engajamento": 0.0},
                "stories": {"quantidade": 0, "engajamento": 0.0},
            },
            "temas_principais": [],
            "hashtags_top": [],
            "hooks_efetivos": [],
        }

    def _default_visual_pattern(self) -> Dict[str, Any]:
        return {
            "paleta_cores": ["#000000", "#FFFFFF", "#D4AF37"],
            "estilo_composicao": "minimalista",
            "tipografia_padrao": "Inter Bold + Regular",
            "elementos_recorrentes": ["badges", "setas", "numeros"],
        }

    def _default_virality_score(self) -> Dict[str, Any]:
        return {
            "score_geral": 0.0,
            "fatores_fortes": [],
            "fatores_fracos": [],
            "recomendacoes": [
                "Analise pelo menos 10 posts para score inicial",
                "Identifique padrões visuais consistentes",
                "Mapeie hooks que funcionam",
            ],
        }
