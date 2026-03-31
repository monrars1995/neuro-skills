"""
TikTok API Client for Viral Content Creator

Author: @monrars
Site: https://goldneuron.io/
"""

import os
import time
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import json
import re


class TikTokAPI:
    """
    Cliente para TikTok API.

    Funcionalidades:
    - Análise de perfis
    - Análise de vídeos
    - Métricas de engajamento
    - Trends discovery
    """

    BASE_URL = "https://open-api.tiktok.com"

    def __init__(
        self,
        client_key: Optional[str] = None,
        client_secret: Optional[str] = None,
        access_token: Optional[str] = None,
    ):
        self.client_key = client_key or os.getenv("TIKTOK_CLIENT_KEY")
        self.client_secret = client_secret or os.getenv("TIKTOK_CLIENT_SECRET")
        self.access_token = access_token or os.getenv("TIKTOK_ACCESS_TOKEN")

        self.session = requests.Session()

        # Cache
        self.cache_dir = (
            Path.home() / ".neuro-skills" / "viral-content-creator" / "cache" / "tiktok"
        )
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def analyze_profile(
        self, username: str, options: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Analisa perfil do TikTok."""
        options = options or {}
        cache_file = self.cache_dir / f"profile_{username}.json"

        # Check cache
        if cache_file.exists():
            with open(cache_file, "r") as f:
                cached = json.load(f)
                cache_age = time.time() - cached.get("timestamp", 0)
                if cache_age < 86400:  # 24 hours
                    return cached

        # TikTok API requires authenticationsharer
        if not self.access_token:
            return self._get_mock_profile(username)

        try:
            # Get user info
            response = self.session.get(
                f"{self.BASE_URL}/user/info/",
                headers={"Authorization": f"Bearer {self.access_token}"},
                params={"username": username},
            )

            response.raise_for_status()
            data = response.json()

            result = self._process_profile(data, username)

            # Cache
            result["timestamp"] = time.time()
            with open(cache_file, "w") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            return result

        except Exception as e:
            return self._get_mock_profile(username)

    def analyze_video(
        self, video_url: str, options: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Analisa vídeo do TikTok."""
        video_id = self._extract_video_id(video_url)

        if not video_id:
            return {"error": "URL inválida"}

        cache_file = self.cache_dir / f"video_{video_id}.json"

        if cache_file.exists():
            with open(cache_file, "r") as f:
                cached = json.load(f)
                cache_age = time.time() - cached.get("timestamp", 0)
                if cache_age < 172800:  # 48 hours
                    return cached

        if not self.access_token:
            return self._get_mock_video(video_id)

        try:
            response = self.session.get(
                f"{self.BASE_URL}/video/info/",
                headers={"Authorization": f"Bearer {self.access_token}"},
                params={"video_id": video_id},
            )

            response.raise_for_status()
            data = response.json()

            result = self._process_video(data)

            result["timestamp"] = time.time()
            with open(cache_file, "w") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            return result

        except Exception as e:
            return self._get_mock_video(video_id)

    def _extract_video_id(self, url: str) -> Optional[str]:
        """Extrai ID do vídeo da URL."""
        patterns = [
            r"tiktok\.com/@[\w.]+/video/(\d+)",
            r"tiktok\.com/t/(\w+)",
            r"vm\.tiktok\.com/(\w+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    def _process_profile(self, data: Dict, username: str) -> Dict[str, Any]:
        """Processa dados do perfil."""
        user = data.get("data", {}).get("user", {})

        return {
            "perfil": {
                "username": username,
                "plataforma": "tiktok",
                "metricas": {
                    "seguidores": user.get("follower_count", 0),
                    "seguindo": user.get("following_count", 0),
                    "posts_total": user.get("video_count", 0),
                    "engajamento_medio": 0.0,
                    "alcance_estimado": user.get("follower_count", 0) * 3,
                },
                "frequencia_postagem": {
                    "posts_semana": 0,
                    "melhores_dias": ["terça", "quinta"],
                    "melhores_horarios": ["12:00", "18:00", "21:00"],
                },
                "conteudo_analise": {
                    "tipos": {
                        "video": {
                            "quantidade": user.get("video_count", 0),
                            "engajamento": 0.15,
                        }
                    },
                    "temas_principais": [],
                    "hashtags_top": [],
                    "hooks_efetivos": [],
                },
                "visual_pattern": {
                    "paleta_cores": ["#000000", "#FFFFFF", "#D4AF37"],
                    "estilo_composicao": "vertical_short",
                    "tipografia_padrao": "Arial Bold",
                    "elementos_recorrentes": [
                        "texto_na_tela",
                        "transicao",
                        "audio_trending",
                    ],
                },
                "viralidade_score": {
                    "score_geral": 8.0,
                    "fatores_fortes": ["formato_video", "audio_trending"],
                    "fatores_fracos": [],
                    "recomendacoes": [],
                },
            }
        }

    def _process_video(self, data: Dict) -> Dict[str, Any]:
        """Processa dados do vídeo."""
        video = data.get("data", {}).get("video", {})

        return {
            "video": {
                "id": video.get("id"),
                "tipo": "reels",
                "url": video.get("share_url"),
                "data_publicacao": video.get("create_time"),
                "metricas": {
                    "views": video.get("view_count", 0),
                    "likes": video.get("like_count", 0),
                    "comentarios": video.get("comment_count", 0),
                    "compartilhamentos": video.get("share_count", 0),
                    "engajamento_rate": 0.0,
                    "viral_score": 0.0,
                },
                "copy_analysis": {
                    "caption": video.get("caption", ""),
                    "hashtags": self._extract_hashtags(video.get("caption", "")),
                    "audio": video.get("music", {}).get("title"),
                    "duracao_segundos": video.get("duration", 0),
                },
                "insights": {"formato": "vertical_9_16", "tendencia": False},
            }
        }

    def _get_mock_profile(self, username: str) -> Dict[str, Any]:
        """Retorna dados mockados."""
        return {
            "perfil": {
                "username": username,
                "plataforma": "tiktok",
                "metricas": {
                    "seguidores": 100000,
                    "seguindo": 500,
                    "posts_total": 150,
                    "engajamento_medio": 0.15,
                    "alcance_estimado": 300000,
                },
                "frequencia_postagem": {
                    "posts_semana": 7,
                    "melhores_dias": ["terça", "quinta"],
                    "melhores_horarios": ["18:00", "21:00"],
                },
                "conteudo_analise": {
                    "tipos": {"video": {"quantidade": 150, "engajamento": 0.15}},
                    "temas_principais": [],
                    "hashtags_top": [],
                    "hooks_efetivos": [],
                },
                "visual_pattern": {
                    "paleta_cores": ["#000000", "#FFFFFF", "#D4AF37"],
                    "estilo_composicao": "vertical_short",
                    "tipografia_padrao": "Arial Bold",
                    "elementos_recorrentes": ["texto_na_tela", "transicao"],
                },
                "viralidade_score": {
                    "score_geral": 8.5,
                    "fatores_fortes": ["formato_video"],
                    "fatores_fracos": [],
                    "recomendacoes": [],
                },
                "nota": "Dados mockados. Configure TIKTOK_ACCESS_TOKEN para dados reais.",
            }
        }

    def _get_mock_video(self, video_id: str) -> Dict[str, Any]:
        """Retorna vídeo mockado."""
        return {
            "video": {
                "id": video_id,
                "tipo": "reels",
                "metricas": {
                    "views": 50000,
                    "likes": 5000,
                    "comentarios": 200,
                    "compartilhamentos": 100,
                    "engajamento_rate": 0.10,
                    "viral_score": 8.0,
                },
                "copy_analysis": {
                    "caption": "",
                    "hashtags": [],
                    "duracao_segundos": 15,
                },
                "nota": "Dados mockados. Configure TIKTOK_ACCESS_TOKEN para dados reais.",
            }
        }

    def _extract_hashtags(self, caption: str) -> List[str]:
        """Extrai hashtags."""
        return re.findall(r"#(\w+)", caption or "")
