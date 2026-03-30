"""
Post Analyzer - Analisa posts específicos para identificar fatores de viralização.

Author: @monrars
"""

import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from urllib.parse import urlparse


@dataclass
class PostMetrics:
    likes: int = 0
    comentarios: int = 0
    compartilhamentos: int = 0
    saves: int = 0
    engajamento_rate: float = 0.0
    viral_score: float = 0.0


@dataclass
class CopyAnalysis:
    estrutura: str = ""
    componentes: Dict[str, Any] = field(default_factory=dict)
    linguagem: Dict[str, Any] = field(default_factory=dict)
    psicologia: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisualAnalysis:
    slides: int = 0
    formato: str = ""
    resolucao: str = ""
    paleta_geral: Dict[str, Any] = field(default_factory=dict)
    tipografia: Dict[str, Any] = field(default_factory=dict)
    composicao: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Template:
    nome: str = ""
    estrutura: List[Dict[str, Any]] = field(default_factory=list)
    score: float = 0.0
    usos_recomendados: List[str] = field(default_factory=list)


class PostAnalyzer:
    """
    Analisa posts específicos para extrair fatores de viralização.

    Suporta:
    - Instagram (posts, carrosséis, reels)
    - TikTok (vídeos)
    - Twitter/X (tweets, threads)
    - LinkedIn (posts)
    - YouTube (vídeos)
    """

    PLATFORM_PATTERNS = {
        "instagram": r"instagram\.com/(p|reel|reels)/[\w-]+",
        "tiktok": r"tiktok\.com/@[\w.]+/video/[\d]+",
        "twitter": r"(twitter|x)\.com/[\w]+/status/[\d]+",
        "linkedin": r"linkedin\.com/posts/[\w-]+",
        "youtube": r"youtube\.com/watch\?v=[\w-]+|youtu\.be/[\w-]+",
    }

    COPY_STRUCTURES = {
        "HOOK_PROBLEM_SOLUTION_CTA": ["hook", "problema", "solucao", "cta"],
        "CONTRASTE_INFORMACAO_BENEFICIO_CTA": [
            "contraste",
            "informacao",
            "beneficio",
            "cta",
        ],
        "DADO_CONTEXTO_APLICACAO_CTA": ["dado", "contexto", "aplicacao", "cta"],
        "STORY_LESSON_ACTION": ["historia", "licao", "acao"],
    }

    HOOK_TYPES = [
        "pergunta_retorica",
        "dado_chocante",
        "conspiracao",
        "promessa",
        "historia_pessoal",
        "contraste",
    ]

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.cache = {}

    def analyze(self, url: str, options: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analisa um post específico.

        Args:
            url: URL do post
            options: Opções de análise

        Returns:
            Dict com análise completa do post
        """
        options = options or {
            "analyze_visual": True,
            "analyze_copy": True,
            "analyze_engagement": True,
            "extract_template": True,
        }

        plataforma = self._detect_platform(url)
        if not plataforma:
            return {"error": "URL não reconhecida"}

        result = {
            "post": {
                "url": url,
                "id": self._extract_post_id(url, plataforma),
                "tipo": self._detect_post_type(url, plataforma),
                "data_publicacao": datetime.now().isoformat(),
                "metricas": self._extract_metrics(url, plataforma),
                "copy_analysis": self._analyze_copy(url, plataforma, options)
                if options.get("analyze_copy")
                else {},
                "visual_analysis": self._analyze_visual(url, plataforma, options)
                if options.get("analyze_visual")
                else {},
                "template_extraido": self._extract_template(url, plataforma)
                if options.get("extract_template")
                else {},
                "timing": self._analyze_timing(url, plataforma),
                "hashtags": self._analyze_hashtags(url, plataforma),
            }
        }

        self.cache[url] = result
        return result

    def _detect_platform(self, url: str) -> Optional[str]:
        """Detecta a plataforma baseado na URL."""
        for plataforma, pattern in self.PLATFORM_PATTERNS.items():
            if re.search(pattern, url, re.IGNORECASE):
                return plataforma
        return None

    def _extract_post_id(self, url: str, plataforma: str) -> str:
        """Extrai ID do post da URL."""
        patterns = {
            "instagram": r"/(p|reel|reels)/([\w-]+)",
            "tiktok": r"/video/([\d]+)",
            "twitter": r"/status/([\d]+)",
            "linkedin": r"/posts/([\w-]+)",
            "youtube": r"(?:v=|youtu\.be/)([\w-]+)",
        }

        pattern = patterns.get(plataforma)
        if pattern:
            match = re.search(pattern, url)
            if match:
                return match.group(2) if plataforma == "instagram" else match.group(1)
        return "unknown"

    def _detect_post_type(self, url: str, plataforma: str) -> str:
        """Detecta o tipo de post."""
        if "reel" in url or "reels" in url:
            return "reels"
        elif "tiktok" in url:
            return "video"
        elif "/p/" in url:
            return "carousel" if "carousel" in url else "static"
        return "post"

    def _extract_metrics(self, url: str, plataforma: str) -> Dict[str, Any]:
        """
        Extrai métricas do post.

        Em produção, chamaria APIs reais.
        """
        return {
            "likes": 0,
            "comentarios": 0,
            "compartilhamentos": 0,
            "saves": 0,
            "engajamento_rate": 0.0,
            "viral_score": 0.0,
            "benchmark": {
                "vs_seguidores": "N/A",
                "vs_industria": "N/A",
                "vs_perfil": "N/A",
            },
            "nota": "Requer integração com API real",
        }

    def _analyze_copy(self, url: str, plataforma: str, options: Dict) -> Dict[str, Any]:
        """Analisa a copy do post."""
        return {
            "estrutura": "HOOK_PROBLEM_SOLUTION_CTA",
            "componentes": {
                "hook": {"texto": "", "tipo": "pergunta_retorica", "score": 0.0},
                "problema": {
                    "texto": "",
                    "tipo": "problema_identificacao",
                    "score": 0.0,
                },
                "solucao": {"texto": "", "tipo": "explicacao", "score": 0.0},
                "cta": {"texto": "", "tipo": "acao_direta", "score": 0.0},
            },
            "linguagem": {
                "tom": "educativo_informal",
                "pronome": "você",
                "emojis_count": 0,
                "hashtags_count": 0,
                "mentions_count": 0,
                "caracteres": 0,
                "palavras": 0,
                "frases": 0,
            },
            "psicologia": {
                "gatilhos": ["curiosidade", "urgência", "valor"],
                "emoções": ["surpresa", "alívio", "satisfação"],
                "cognitive_load": "baixo",
            },
            "nota": "Requer texto real do post",
        }

    def _analyze_visual(
        self, url: str, plataforma: str, options: Dict
    ) -> Dict[str, Any]:
        """Analisa elementos visuais do post."""
        return {
            "slides": 1,
            "formato": "4:5",
            "resolucao": "1080x1350",
            "paleta_geral": {
                "cores_primarias": ["#000000", "#FFFFFF", "#D4AF37"],
                "cores_secundarias": ["#1A1A25", "#2A2A3A"],
                "temperatura": "fria",
                "contraste": "alto",
            },
            "tipografia": {
                "headline": {"fonte": "Inter", "peso": 700, "tamanho": 48},
                "body": {"fonte": "Inter", "peso": 400, "tamanho": 24},
                "cta": {"fonte": "Inter", "peso": 600, "tamanho": 20},
            },
            "composicao": {
                "regra_tercos": True,
                "espaco_negativo": 40,
                "alinheamento": "centralizado",
                "fluxo_leitura": "top_down",
            },
            "nota": "Requer análise de imagem real",
        }

    def _extract_template(self, url: str, plataforma: str) -> Dict[str, Any]:
        """Extrai template do post."""
        return {
            "nome": "template_generico",
            "estrutura": [],
            "score": 0.0,
            "usos_recomendados": [],
            "nota": "Requer mais posts para template",
        }

    def _analyze_timing(self, url: str, plataforma: str) -> Dict[str, Any]:
        """Analisa timing do post."""
        return {
            "dia_semana": "quarta",
            "hora": "12:00",
            "timezone": "America/Sao_Paulo",
            "razao": "horário de almoço, maior engajamento",
            "nota": "Requer dados reais do post",
        }

    def _analyze_hashtags(self, url: str, plataforma: str) -> Dict[str, Any]:
        """Analisa hashtags do post."""
        return {
            "usadas": [],
            "performance": {},
            "sugestoes": [],
            "nota": "Requer texto real do post",
        }

    def analyze_batch(
        self, urls: List[str], options: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Analisa múltiplos posts em lote."""
        results = {}
        for url in urls:
            results[url] = self.analyze(url, options)
        return results

    def get_top_performing(
        self, urls: List[str], metric: str = "viral_score"
    ) -> Dict[str, Any]:
        """Retorna posts com melhor performance."""
        if not self.cache:
            for url in urls:
                self.analyze(url)

        sorted_posts = sorted(
            self.cache.items(),
            key=lambda x: x[1]["post"]["metricas"].get(metric, 0),
            reverse=True,
        )

        return {"top_posts": [p[0] for p in sorted_posts[:10]], "metric": metric}

    def compare_posts(self, urls: List[str]) -> Dict[str, Any]:
        """Compara múltiplos posts."""
        if len(urls) < 2:
            return {"error": "Necessário pelo menos 2 posts para comparação"}

        return {
            "comparacao": {url: self.analyze(url) for url in urls},
            "insights": [
                "Compare os elementos que diferem",
                "Identifique padrões comuns nos melhores",
                "Extraia o que funciona e o que não funciona",
            ],
        }


# Padrões de copy reconhecidos
COPY_PATTERNS = {
    "hook_patterns": [
        r"Você (sabia|já percebeu|notou)",
        r"Por que \d+% (das pessoas|dos|das)",
        r"A (maioria|minoridade) (não|nada|ninguém)",
        r"(O|A|Os|As) (banco|vendedor|empresa) (não|NÃO)",
        r"\d+ (coisas|motivos|razões|erros)",
    ],
    "cta_patterns": [
        r"(Salva|Salvar|Salve)( pra| para| agora)?",
        r"(Comenta|Comente) (SIM|X|qualquer coisa)",
        r"(Manda|Envia|Envie) (para|pro) (amigo|amiga)",
        r"(Segue|Siga) (para|pra)",
    ],
}
