"""
Instagram Graph API client for Viral Content Creator.

Uses the Meta Graph API when credentials are available and falls back to
sample data when discovery is unavailable.
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


class InstagramAPI:
    API_VERSION = "v21.0"
    BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

    def __init__(
        self,
        access_token: Optional[str] = None,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
    ):
        self.access_token = access_token or os.getenv("META_ACCESS_TOKEN")
        self.app_id = app_id or os.getenv("META_APP_ID")
        self.app_secret = app_secret or os.getenv("META_APP_SECRET")
        self.session = requests.Session()
        if self.access_token:
            self.session.params = {"access_token": self.access_token}
        self.cache_dir = (
            Path.home()
            / ".neuro-skills"
            / "viral-content-creator"
            / "cache"
            / "instagram"
        )
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def analyze_profile(
        self, username: str, options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        options = options or {}
        username = self._normalize_username(username)
        cached = self._load_cache(f"profile_{username}", 86400)
        if cached:
            return cached

        if not self.access_token:
            return self._get_mock_profile(username)

        discovery = self._business_discovery(username, options.get("posts_limit", 25))
        if "error" in discovery:
            return self._get_mock_profile(username, note=discovery["error"])

        result = self._process_discovery_profile(discovery)
        self._save_cache(f"profile_{username}", result)
        return result

    def analyze_post(
        self, post_url: str, options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        _ = options or {}
        shortcode = self._extract_shortcode(post_url)
        if not shortcode:
            return {"error": "URL inválida ou shortcode não encontrado"}

        cached = self._load_cache(f"post_{shortcode}", 172800)
        if cached:
            return cached

        if not self.access_token:
            return self._get_mock_post(shortcode, post_url)

        # Direct shortcode lookup is not available in Graph API for arbitrary posts,
        # so we expose a graceful fallback until a mapped IG user/media ID is available.
        return self._get_mock_post(
            shortcode,
            post_url,
            note="Graph API requires a mapped media ID or business discovery source for this post.",
        )

    def _business_discovery(self, username: str, posts_limit: int) -> Dict[str, Any]:
        fields = (
            f"business_discovery.username({username})"
            "{id,username,name,biography,followers_count,follows_count,media_count,"
            f"media.limit({posts_limit})"
            "{id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count}}"
        )
        return self._make_request("me", {"fields": fields})

    def _make_request(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            response = self.session.get(
                f"{self.BASE_URL}/{endpoint}", params=params, timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as exc:
            try:
                payload = exc.response.json()
                message = payload.get("error", {}).get("message", str(exc))
            except Exception:
                message = str(exc)
            return {"error": message}
        except requests.exceptions.RequestException as exc:
            return {"error": f"Erro de conexão: {exc}"}

    def _process_discovery_profile(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        discovery = payload.get("business_discovery", {})
        media = discovery.get("media", {}).get("data", [])
        followers = discovery.get("followers_count", 0)
        avg_engagement = self._average(
            [
                item.get("like_count", 0) + item.get("comments_count", 0)
                for item in media
            ]
        )
        avg_engagement_rate = (
            round((avg_engagement / followers), 4) if followers else 0.0
        )
        type_counts = self._count_media_types(media)
        best_hours = self._best_hours(media)
        best_days = self._best_days(media)

        return {
            "perfil": {
                "username": discovery.get("username"),
                "plataforma": "instagram",
                "metricas": {
                    "seguidores": followers,
                    "seguindo": discovery.get("follows_count", 0),
                    "posts_total": discovery.get("media_count", 0),
                    "engajamento_medio": avg_engagement_rate,
                    "alcance_estimado": int(followers * 1.8),
                },
                "frequencia_postagem": {
                    "posts_semana": round(self._posts_per_week(media), 1),
                    "melhores_dias": best_days,
                    "melhores_horarios": best_hours,
                },
                "conteudo_analise": {
                    "tipos": {
                        "carousel": {
                            "quantidade": type_counts.get("CAROUSEL_ALBUM", 0),
                            "engajamento": avg_engagement_rate,
                        },
                        "reels": {
                            "quantidade": type_counts.get("VIDEO", 0),
                            "engajamento": avg_engagement_rate,
                        },
                        "static": {
                            "quantidade": type_counts.get("IMAGE", 0),
                            "engajamento": avg_engagement_rate,
                        },
                        "stories": {"quantidade": 0, "engajamento": 0.0},
                    },
                    "temas_principais": self._top_caption_terms(media),
                    "hashtags_top": self._top_hashtags(media),
                    "hooks_efetivos": self._top_hooks(media),
                },
                "visual_pattern": {
                    "paleta_cores": ["#000000", "#FFFFFF", "#D4AF37"],
                    "estilo_composicao": "minimalista",
                    "tipografia_padrao": "Inter Bold + Regular",
                    "elementos_recorrentes": ["badges", "setas", "numeros"],
                },
                "viralidade_score": self._virality_score(media, followers),
            }
        }

    def _virality_score(
        self, media: List[Dict[str, Any]], followers: int
    ) -> Dict[str, Any]:
        if not media or not followers:
            return {
                "score_geral": 0.0,
                "fatores_fortes": [],
                "fatores_fracos": ["dados insuficientes"],
                "recomendacoes": [
                    "Conecte uma conta business com mídia acessível via Graph API."
                ],
            }

        avg_rate = self._average(
            [
                (item.get("like_count", 0) + item.get("comments_count", 0)) / followers
                for item in media
            ]
        )
        viral_posts = sum(
            1
            for item in media
            if (item.get("like_count", 0) + item.get("comments_count", 0))
            > (avg_rate * followers * 2)
        )
        score = min(
            10.0, round((avg_rate * 60) + (viral_posts / max(len(media), 1) * 4), 1)
        )
        return {
            "score_geral": score,
            "fatores_fortes": ["engajamento", "consistência"]
            if score >= 6
            else ["volume"],
            "fatores_fracos": [] if score >= 6 else ["baixo engajamento relativo"],
            "recomendacoes": [
                "Replicar os hooks com maior taxa de curtidas e comentários.",
                "Concentrar testes nos horários com melhor resposta.",
                "Priorizar carrosséis e vídeos se já performam acima da média.",
            ],
        }

    def _top_hashtags(self, media: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        counts: Dict[str, int] = {}
        for item in media:
            for hashtag in re.findall(r"#(\w+)", item.get("caption", "")):
                counts[hashtag.lower()] = counts.get(hashtag.lower(), 0) + 1
        return [
            {"tag": f"#{tag}", "usos": uses, "engajamento_medio": 0.0}
            for tag, uses in sorted(
                counts.items(), key=lambda pair: pair[1], reverse=True
            )[:10]
        ]

    def _top_caption_terms(self, media: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        stopwords = {
            "de",
            "da",
            "do",
            "e",
            "a",
            "o",
            "que",
            "para",
            "com",
            "em",
            "um",
            "uma",
            "pra",
        }
        counts: Dict[str, int] = {}
        for item in media:
            words = re.findall(r"[A-Za-zÀ-ÿ0-9_]+", item.get("caption", "").lower())
            for word in words:
                if len(word) > 3 and word not in stopwords and not word.startswith("#"):
                    counts[word] = counts.get(word, 0) + 1
        return [
            {"tema": word, "frequencia": count / max(len(media), 1), "engajamento": 0.0}
            for word, count in sorted(
                counts.items(), key=lambda pair: pair[1], reverse=True
            )[:10]
        ]

    def _top_hooks(self, media: List[Dict[str, Any]]) -> List[str]:
        hooks: List[str] = []
        for item in media:
            caption = item.get("caption", "").strip()
            if caption:
                first_line = caption.splitlines()[0].strip()
                if first_line:
                    hooks.append(first_line[:120])
        return hooks[:10]

    def _count_media_types(self, media: List[Dict[str, Any]]) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for item in media:
            media_type = item.get("media_type", "IMAGE")
            counts[media_type] = counts.get(media_type, 0) + 1
        return counts

    def _posts_per_week(self, media: List[Dict[str, Any]]) -> float:
        timestamps = [item.get("timestamp") for item in media if item.get("timestamp")]
        if len(timestamps) < 2:
            return float(len(media))
        dates = [self._parse_date(ts) for ts in timestamps]
        days = max((max(dates) - min(dates)).days, 1)
        return (len(media) / days) * 7

    def _best_hours(self, media: List[Dict[str, Any]]) -> List[str]:
        hours: Dict[str, int] = {}
        for item in media:
            ts = item.get("timestamp")
            if not ts:
                continue
            hour = self._parse_date(ts).strftime("%H:00")
            hours[hour] = hours.get(hour, 0) + 1
        return [
            hour
            for hour, _ in sorted(
                hours.items(), key=lambda pair: pair[1], reverse=True
            )[:3]
        ] or ["12:00"]

    def _best_days(self, media: List[Dict[str, Any]]) -> List[str]:
        days: Dict[str, int] = {}
        for item in media:
            ts = item.get("timestamp")
            if not ts:
                continue
            day = self._parse_date(ts).strftime("%A").lower()
            days[day] = days.get(day, 0) + 1
        mapped = {
            "monday": "segunda",
            "tuesday": "terça",
            "wednesday": "quarta",
            "thursday": "quinta",
            "friday": "sexta",
            "saturday": "sábado",
            "sunday": "domingo",
        }
        return [
            mapped.get(day, day)
            for day, _ in sorted(days.items(), key=lambda pair: pair[1], reverse=True)[
                :3
            ]
        ] or ["quarta"]

    def _average(self, values: List[float]) -> float:
        return sum(values) / len(values) if values else 0.0

    def _parse_date(self, value: str):
        return __import__("datetime").datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )

    def _extract_shortcode(self, url: str) -> Optional[str]:
        match = re.search(r"instagram\.com/(?:p|reel|reels|tv)/([\w-]+)", url)
        return match.group(1) if match else None

    def _normalize_username(self, username: str) -> str:
        username = username.strip()
        if username.startswith("@"):
            return username[1:]
        match = re.search(r"instagram\.com/([\w.]+)", username)
        return match.group(1) if match else username

    def _load_cache(self, key: str, ttl_seconds: int) -> Optional[Dict[str, Any]]:
        cache_file = self.cache_dir / f"{key}.json"
        if not cache_file.exists():
            return None
        with open(cache_file, "r", encoding="utf-8") as handle:
            cached = json.load(handle)
        if (time.time() - cached.get("timestamp", 0)) < ttl_seconds:
            return cached
        return None

    def _save_cache(self, key: str, payload: Dict[str, Any]) -> None:
        cache_file = self.cache_dir / f"{key}.json"
        data = dict(payload)
        data["timestamp"] = time.time()
        with open(cache_file, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)

    def _get_mock_profile(
        self, username: str, note: Optional[str] = None
    ) -> Dict[str, Any]:
        payload = {
            "perfil": {
                "username": username,
                "plataforma": "instagram",
                "metricas": {
                    "seguidores": 50000,
                    "seguindo": 200,
                    "posts_total": 342,
                    "engajamento_medio": 0.08,
                    "alcance_estimado": 150000,
                },
                "frequencia_postagem": {
                    "posts_semana": 5,
                    "melhores_dias": ["terça", "quinta", "sábado"],
                    "melhores_horarios": ["12:00", "19:00", "21:00"],
                },
                "conteudo_analise": {
                    "tipos": {
                        "carousel": {"quantidade": 120, "engajamento": 0.12},
                        "reels": {"quantidade": 80, "engajamento": 0.15},
                        "static": {"quantidade": 100, "engajamento": 0.05},
                        "stories": {"quantidade": 42, "engajamento": 0.03},
                    },
                    "temas_principais": [],
                    "hashtags_top": [],
                    "hooks_efetivos": [],
                },
                "visual_pattern": {
                    "paleta_cores": ["#000000", "#FFFFFF", "#D4AF37"],
                    "estilo_composicao": "minimalista",
                    "tipografia_padrao": "Inter Bold + Regular",
                    "elementos_recorrentes": ["badges", "setas", "numeros"],
                },
                "viralidade_score": {
                    "score_geral": 7.5,
                    "fatores_fortes": ["engajamento", "consistência"],
                    "fatores_fracos": [],
                    "recomendacoes": ["Aumentar frequência", "Testar mais formatos"],
                },
                "nota": note or "Configure META_ACCESS_TOKEN para dados reais.",
            }
        }
        return payload

    def _get_mock_post(
        self, shortcode: str, url: str, note: Optional[str] = None
    ) -> Dict[str, Any]:
        return {
            "post": {
                "id": shortcode,
                "tipo": "reels" if "/reel/" in url or "/reels/" in url else "carousel",
                "url": url,
                "data_publicacao": None,
                "metricas": {
                    "likes": 4200,
                    "comentarios": 180,
                    "compartilhamentos": 0,
                    "saves": 0,
                    "engajamento_rate": 0.0,
                    "viral_score": 7.5,
                },
                "copy_analysis": {
                    "caption": "",
                    "hashtags": [],
                    "mentions": [],
                    "estrutura": "GENERIC",
                },
                "insights": {},
                "nota": note
                or "Configure mapeamento de mídia para dados reais do post.",
            }
        }
