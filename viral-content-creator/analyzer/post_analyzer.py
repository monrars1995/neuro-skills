"""Post analyzer with platform-specific API delegation."""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.instagram_api import InstagramAPI
from api.tiktok_api import TikTokAPI
from api.twitter_api import TwitterAPI


class PostAnalyzer:
    PLATFORM_PATTERNS = {
        "instagram": r"instagram\.com/(p|reel|reels)/[\w-]+",
        "tiktok": r"tiktok\.com/@[\w.]+/video/[\d]+",
        "twitter": r"(twitter|x)\.com/[\w]+/status/[\d]+",
        "linkedin": r"linkedin\.com/posts/[\w-]+",
        "youtube": r"youtube\.com/watch\?v=[\w-]+|youtu\.be/[\w-]+",
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.cache: Dict[str, Dict[str, Any]] = {}
        self._instagram = InstagramAPI()
        self._tiktok = TikTokAPI()
        self._twitter = TwitterAPI()

    def analyze(
        self, url: str, options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        options = options or {}
        plataforma = self._detect_platform(url)
        if not plataforma:
            return {"error": "URL não reconhecida"}

        result = self._fetch_platform_post(url, plataforma, options)
        if result:
            self.cache[url] = result
            return result

        fallback = {
            "post": {
                "url": url,
                "id": self._extract_post_id(url, plataforma),
                "tipo": self._detect_post_type(url, plataforma),
                "data_publicacao": datetime.now().isoformat(),
                "metricas": {
                    "likes": 0,
                    "comentarios": 0,
                    "compartilhamentos": 0,
                    "saves": 0,
                    "engajamento_rate": 0.0,
                    "viral_score": 0.0,
                },
                "copy_analysis": {
                    "estrutura": "GENERIC",
                    "caption": "",
                    "hashtags": [],
                    "mentions": [],
                },
                "visual_analysis": {
                    "nota": "Sem análise visual real para esta plataforma."
                },
                "template_extraido": {
                    "nome": "template_generico",
                    "estrutura": [],
                    "score": 0.0,
                },
                "timing": {"dia_semana": "quarta", "hora": "12:00"},
                "hashtags": {"usadas": [], "performance": {}, "sugestoes": []},
                "nota": f"Integração real ainda não disponível para {plataforma}.",
            }
        }
        self.cache[url] = fallback
        return fallback

    def _fetch_platform_post(
        self, url: str, plataforma: str, options: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        if plataforma == "instagram":
            return self._instagram.analyze_post(url, options)
        if plataforma == "tiktok":
            return self._tiktok.analyze_video(url, options)
        if plataforma == "twitter":
            return self._twitter.analyze_tweet(url, options)
        return None

    def _detect_platform(self, url: str) -> Optional[str]:
        for plataforma, pattern in self.PLATFORM_PATTERNS.items():
            if re.search(pattern, url, re.IGNORECASE):
                return plataforma
        return None

    def _extract_post_id(self, url: str, plataforma: str) -> str:
        patterns = {
            "instagram": r"/(p|reel|reels)/([\w-]+)",
            "tiktok": r"/video/([\d]+)",
            "twitter": r"/status/([\d]+)",
            "linkedin": r"/posts/([\w-]+)",
            "youtube": r"(?:v=|youtu\.be/)([\w-]+)",
        }
        pattern = patterns.get(plataforma)
        if not pattern:
            return "unknown"
        match = re.search(pattern, url)
        if not match:
            return "unknown"
        return match.group(2) if plataforma == "instagram" else match.group(1)

    def _detect_post_type(self, url: str, plataforma: str) -> str:
        if plataforma == "instagram" and ("/reel/" in url or "/reels/" in url):
            return "reels"
        if plataforma == "tiktok":
            return "video"
        if plataforma == "twitter":
            return "tweet"
        if "/p/" in url:
            return "carousel"
        return "post"
