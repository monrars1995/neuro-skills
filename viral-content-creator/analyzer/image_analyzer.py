"""
Image Analyzer - Analisa imagens para identificar padrões visuais.

Author: @monrars
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import re


@dataclass
class ColorPalette:
    cores_primarias: List[Dict[str, Any]] = field(default_factory=list)
    temperatura: str = "fria"
    saturacao: str = "baixa"
    luminosidade: str = "baixa"
    contraste: str = "alto"
    harmonia: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TypographyInfo:
    fontes_detectadas: List[Dict[str, Any]] = field(default_factory=list)
    tamanhos: Dict[str, int] = field(default_factory=dict)
    hierarquia: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    legibilidade: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CompositionInfo:
    regra_tercos: Dict[str, Any] = field(default_factory=dict)
    direcao_leitura: Dict[str, str] = field(default_factory=dict)
    espaco_negativo: Dict[str, Any] = field(default_factory=dict)
    foco: Dict[str, Any] = field(default_factory=dict)


class ImageAnalyzer:
    """
    Analisa imagens para extrair padrões visuais.

    Funcionalidades:
    - Extração de paleta de cores
    - Detecção de tipografia
    - Análise de composição
    - Score visual
    """

    BRAND_COLORS = {
        "primary": "#D4AF37",  # Dourado
        "secondary": "#000000",  # Preto
        "background": "#0A0A0F",  # Preto profundo
        "text": "#FFFFFF",  # Branco
    }

    DEFAULT_FONTS = {
        "headline": {"fonte": "Inter", "peso": 700, "tamanho": 48},
        "body": {"fonte": "Inter", "peso": 400, "tamanho": 24},
        "cta": {"fonte": "Inter", "peso": 600, "tamanho": 20},
    }

    ELEMENT_TYPES = [
        "badge",
        "seta",
        "icone",
        "numero",
        "grafico",
        "tabela",
        "borda",
        "sombra",
    ]

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.cache = {}

    def analyze(
        self, image_source: str, options: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Analisa uma imagem.

        Args:
            image_source: URL ou base64 da imagem
            options: Opções de análise

        Returns:
            Dict com análise completa da imagem
        """
        options = options or {
            "extract_palette": True,
            "detect_text": True,
            "detect_elements": True,
            "analyze_composition": True,
            "score_visual": True,
        }

        result = {
            "imagem": {
                "dimensoes": self._get_dimensions(image_source),
                "paleta": self._extract_palette(image_source, options)
                if options.get("extract_palette")
                else {},
                "tipografia": self._detect_typography(image_source, options)
                if options.get("detect_text")
                else {},
                "elementos": self._detect_elements(image_source, options)
                if options.get("detect_elements")
                else {},
                "composicao": self._analyze_composition(image_source, options)
                if options.get("analyze_composition")
                else {},
                "score_visual": self._calculate_visual_score(image_source, options)
                if options.get("score_visual")
                else {},
                "match_modelo": self._match_model(image_source),
            }
        }

        self.cache[image_source] = result
        return result

    def _get_dimensions(self, image_source: str) -> Dict[str, Any]:
        """
        Obtém dimensões da imagem.

        Em produção, usaria biblioteca de imagem real.
        """
        is_base64 = image_source.startswith("data:") or len(image_source) > 1000

        return {
            "largura": 1080,
            "altura": 1350,
            "formato": "4:5",
            "resolucao": "alta",
            "source_type": "base64" if is_base64 else "url",
            "nota": "Dimensões padrão - requer imagem real",
        }

    def _extract_palette(self, image_source: str, options: Dict) -> Dict[str, Any]:
        """
        Extrai paleta de cores da imagem.

        Em produção, usaria análise de pixel real.
        """
        return {
            "cores_primarias": [
                {"hex": "#000000", "nome": "Black", "porcentagem": 45},
                {"hex": "#FFFFFF", "nome": "White", "porcentagem": 35},
                {"hex": "#D4AF37", "nome": "Gold", "porcentagem": 15},
                {"hex": "#1A1A25", "nome": "Dark Blue", "porcentagem": 5},
            ],
            "temperatura": "fria",
            "saturacao": "baixa",
            "luminosidade": "baixa",
            "contraste": "alto",
            "harmonia": {
                "tipo": "complementar",
                "score": 8.5,
                "recomendacao": "Paleta equilibrada com destaque dourado",
            },
            "brand_match": self._check_brand_match(),
            "nota": "Paleta padrão - requer análise real",
        }

    def _check_brand_match(self) -> Dict[str, Any]:
        """Verifica se a paleta corresponde às cores da marca."""
        return {
            "match": True,
            "cores_match": ["#D4AF37", "#000000", "#FFFFFF"],
            "recomendacao": "Paleta consistente com a marca GoldNeuron",
        }

    def _detect_typography(self, image_source: str, options: Dict) -> Dict[str, Any]:
        """
        Detecta tipografia na imagem.

        Em produção, usaria OCR e análise de fonte.
        """
        return {
            "fontes_detectadas": [
                {"nome": "Inter", "peso": "bold", "confiança": 0.95},
                {"nome": "Inter", "peso": "regular", "confiança": 0.92},
            ],
            "tamanhos": {"headline": 48, "body": 24, "cta": 20},
            "hierarquia": {
                "nivel_1": {"texto": "Headline", "tamanho": 48, "peso": "bold"},
                "nivel_2": {"texto": "Subtítulo", "tamanho": 24, "peso": "regular"},
                "nivel_3": {"texto": "CTA", "tamanho": 20, "peso": "semibold"},
            },
            "legibilidade": {
                "score": 9.0,
                "problemas": [],
                "recomendacoes": [
                    "Excelente contraste",
                    "Tamanho adequado para mobile",
                    "Hierarquia clara",
                ],
            },
            "nota": "Tipografia padrão - requer análise real",
        }

    def _detect_elements(self, image_source: str, options: Dict) -> Dict[str, Any]:
        """
        Detecta elementos visuais na imagem.

        Em produção, usaria visão computacional.
        """
        return {
            "detectados": [
                {"tipo": "badge", "quantidade": 1, "posicao": "top-right"},
                {"tipo": "seta", "quantidade": 2, "posicao": "bottom-center"},
                {"tipo": "icone", "quantidade": 3, "posicao": "distributed"},
                {"tipo": "numero", "quantidade": 1, "posicao": "center"},
            ],
            "proporcao_elementos": {
                "texto": 60,
                "espaco_negativo": 25,
                "elementos_visuais": 15,
            },
            "nota": "Elementos padrão - requer análise real",
        }

    def _analyze_composition(self, image_source: str, options: Dict) -> Dict[str, Any]:
        """
        Analisa composição da imagem.

        Em produção, usaria análise geométrica real.
        """
        return {
            "regra_tercos": {
                "aplicada": True,
                "ponto_focal": "center-top",
                "score": 8.5,
            },
            "direcao_leitura": {
                "principal": "diagonal-descendente",
                "secundaria": "top-bottom",
            },
            "espaco_negativo": {
                "porcentagem": 40,
                "distribuicao": "balanced",
                "score": 8.0,
            },
            "foco": {
                "tipo": "center-weighted",
                "intensidade": "alto",
                "clarity": "muito claro",
            },
            "nota": "Composição padrão - requer análise real",
        }

    def _calculate_visual_score(
        self, image_source: str, options: Dict
    ) -> Dict[str, Any]:
        """
        Calcula score visual geral.

        Em produção, combinaria todas as análises.
        """
        scores = {
            "paleta": 9.0,
            "tipografia": 9.0,
            "composicao": 8.5,
            "legibilidade": 9.0,
            "atração": 8.0,
        }

        geral = sum(scores.values()) / len(scores)

        return {
            "geral": round(geral, 1),
            "componentes": scores,
            "problemas_detectados": [],
            "sugestoes": [
                "Adicionar elemento surpresa no canto inferior",
                "Considerar adicionar mais contraste no CTA",
                "Testar variação com número maior",
            ],
            "nota": "Score calculado com valores padrão",
        }

    def _match_model(self, image_source: str) -> Dict[str, Any]:
        """Verifica compatibilidade com modelos existentes."""
        return {
            "modelo": "template_educativo",
            "compatibilidade": 0.92,
            "ajustes_necessarios": [],
            "nota": "Match com modelo padrão",
        }

    def analyze_batch(
        self, images: List[str], options: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Analisa múltiplas imagens em lote."""
        results = {}
        for img in images:
            results[img] = self.analyze(img, options)
        return results

    def extract_palette_from_url(self, url: str) -> Dict[str, Any]:
        """Extrai paleta de cores de URL."""
        return self._extract_palette(url, {"extract_palette": True})

    def compare_images(self, image1: str, image2: str) -> Dict[str, Any]:
        """Compara duas imagens."""
        analysis1 = self.analyze(image1)
        analysis2 = self.analyze(image2)

        return {
            "imagem1": analysis1,
            "imagem2": analysis2,
            "diferencas": self._find_differences(analysis1, analysis2),
            "similaridades": self._find_similarities(analysis1, analysis2),
        }

    def _find_differences(self, img1: Dict, img2: Dict) -> List[str]:
        """Encontra diferenças entre duas imagens."""
        return ["Comparar paletas", "Comparar composição", "Comparar tipografia"]

    def _find_similarities(self, img1: Dict, img2: Dict) -> List[str]:
        """Encontra similaridades entre duas imagens."""
        return ["Verificar elementos comuns", "Identificar padrões recorrentes"]

    def suggest_improvements(self, image_source: str) -> Dict[str, Any]:
        """Sugere melhorias para a imagem."""
        analysis = self.analyze(image_source)
        score = analysis["imagem"]["score_visual"]["geral"]

        improvements = []

        if score < 8.0:
            improvements.append("Aumentar contraste geral")

        if score < 7.0:
            improvements.extend(
                [
                    "Revisar hierarquia visual",
                    "Adicionar ponto focal claro",
                    "Reduzir ruído visual",
                ]
            )

        return {
            "score_atual": score,
            "melhorias": improvements,
            "prioridade": "alta"
            if score < 7.0
            else "média"
            if score < 8.0
            else "baixa",
        }


# Padrões visuais pré-definidos
VISUAL_PATTERNS = {
    "minimalista": {"espaco_negativo": 50, "elementos": 3, "cores": 3},
    "maximalista": {"espaco_negativo": 20, "elementos": 10, "cores": 7},
    "documental": {"espaco_negativo": 30, "elementos": 5, "cores": 4},
}
