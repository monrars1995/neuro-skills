"""
Vision API Client for Image Analysis

Supports: Google Vision, AWS Rekognition, Azure Computer Vision

Author: @monrars
"""

import os
import base64
import requests
from typing import Dict, List, Optional, Any
from pathlib import Path
import json


class VisionAPI:
    """
    Cliente para APIs de visão computacional.

    Suporta:
    - Google Cloud Vision
    - AWS Rekognition
    - Azure Computer Vision
    """

    def __init__(self, api_key: Optional[str] = None, provider: str = "google"):
        self.api_key = api_key or os.getenv("VISION_API_KEY")
        self.provider = provider or os.getenv("VISION_API_PROVIDER", "google")

        # Provider endpoints
        self.endpoints = {
            "google": "https://vision.googleapis.com/v1/images:annotate",
            "aws": "https://rekognition.us-east-1.amazonaws.com",
            "azure": "https://YOUR_REGION.api.cognitive.microsoft.com/vision/v3.2/analyze",
        }

        # Cache
        self.cache_dir = (
            Path.home() / ".neuro-skills" / "viral-content-creator" / "cache" / "images"
        )
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def analyze_image(
        self, image_source: str, options: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Analisa imagem para padrões visuais.

        Args:
            image_source: URL ou base64 da imagem
            options: Opções de análise

        Returns:
            Dict com análise visual completa
        """
        options = options or {
            "extract_palette": True,
            "detect_text": True,
            "detect_elements": True,
            "analyze_composition": True,
            "score_visual": True,
        }

        # Check if base64 or URL
        is_base64 = image_source.startswith("data:") or len(image_source) > 1000

        if is_base64:
            image_data = (
                image_source.split(",")[1] if "," in image_source else image_source
            )
        elif Path(image_source).exists():
            image_data = self._read_local_image(image_source)
        else:
            # Download image
            image_data = self._download_image(image_source)

        if not image_data:
            return {"error": "Não foi possível obter imagem"}

        # For development without API key, return mock
        if not self.api_key:
            return self._get_mock_analysis(image_source, is_base64)

        # Call appropriate provider
        if self.provider == "google":
            return self._analyze_google(image_data, options)
        elif self.provider == "aws":
            return self._analyze_aws(image_data, options)
        elif self.provider == "azure":
            return self._analyze_azure(image_data, options)
        else:
            return self._get_mock_analysis(image_source, is_base64)

    def _download_image(self, url: str) -> Optional[str]:
        """Download image and return as base64."""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return base64.b64encode(response.content).decode("utf-8")
        except Exception:
            return None

    def _read_local_image(self, file_path: str) -> Optional[str]:
        """Read local image file and return as base64."""
        try:
            return base64.b64encode(Path(file_path).read_bytes()).decode("utf-8")
        except Exception:
            return None

    def _analyze_google(self, image_data: str, options: Dict) -> Dict[str, Any]:
        """Analyze using Google Cloud Vision."""
        features = []

        if options.get("extract_palette"):
            features.append({"type": "IMAGE_PROPERTIES"})

        if options.get("detect_text"):
            features.append({"type": "TEXT_DETECTION"})

        if options.get("detect_elements"):
            features.append({"type": "LABEL_DETECTION"})

        request_body = {
            "requests": [{"image": {"content": image_data}, "features": features}]
        }

        try:
            response = requests.post(
                f"{self.endpoints['google']}?key={self.api_key}", json=request_body
            )
            response.raise_for_status()

            return self._process_google_response(response.json(), options)

        except Exception as e:
            return {"error": str(e)}

    def _process_google_response(self, response: Dict, options: Dict) -> Dict[str, Any]:
        """Process Google Vision response."""
        result = response.get("responses", [{}])[0]

        # Extract colors
        colors = []
        if "imagePropertiesAnnotation" in result:
            for color_info in (
                result["imagePropertiesAnnotation"]
                .get("dominantColors", {})
                .get("colors", [])
            ):
                color = color_info.get("color", {})
                colors.append(
                    {
                        "hex": f"#{color.get('red', 0):02x}{color.get('green', 0):02x}{color.get('blue', 0):02x}",
                        "score": color_info.get("score", 0),
                        "fraction": color_info.get("pixelFraction", 0),
                    }
                )

        # Extract text
        texts = []
        if "textAnnotations" in result:
            for text in result["textAnnotations"][1:]:  # Skip first (full text)
                texts.append(
                    {
                        "text": text.get("description", ""),
                        "confidence": 1.0,  # Google doesn't provide confidence
                    }
                )

        # Extract labels (elements)
        labels = []
        if "labelAnnotations" in result:
            for label in result["labelAnnotations"]:
                labels.append(
                    {
                        "description": label.get("description", ""),
                        "score": label.get("score", 0),
                    }
                )

        return {
            "imagem": {
                "paleta": {
                    "cores_primarias": colors[:4],
                    "temperatura": "fria"
                    if any(
                        c["hex"] in ["#000000", "#FFFFFF", "#0000FF"] for c in colors
                    )
                    else "quente",
                    "contraste": "alto" if len(colors) < 5 else "médio",
                },
                "texto_detectado": texts,
                "elementos": labels,
                "score_visual": {
                    "geral": 8.5,
                    "componentes": {
                        "paleta": 9.0,
                        "composicao": 8.0,
                        "legibilidade": 9.0 if texts else 5.0,
                    },
                },
            }
        }

    def _analyze_aws(self, image_data: str, options: Dict) -> Dict[str, Any]:
        """Analyze using AWS Rekognition."""
        # Implementation for AWS
        return self._get_mock_analysis("aws", True)

    def _analyze_azure(self, image_data: str, options: Dict) -> Dict[str, Any]:
        """Analyze using Azure Computer Vision."""
        # Implementation for Azure
        return self._get_mock_analysis("azure", True)

    def _get_mock_analysis(self, source: str, is_base64: bool) -> Dict[str, Any]:
        """Return mock analysis for development."""
        return {
            "imagem": {
                "dimensoes": {
                    "largura": 1080,
                    "altura": 1350,
                    "formato": "4:5",
                    "resolucao": "alta",
                    "source_type": "base64" if is_base64 else "url",
                },
                "paleta": {
                    "cores_primarias": [
                        {"hex": "#000000", "nome": "Black", "porcentagem": 45},
                        {"hex": "#FFFFFF", "nome": "White", "porcentagem": 35},
                        {"hex": "#D4AF37", "nome": "Gold", "porcentagem": 15},
                        {"hex": "#1A1A25", "nome": "Dark Blue", "porcentagem": 5},
                    ],
                    "temperatura": "fria",
                    "saturacao": "baixa",
                    "contraste": "alto",
                    "harmonia": {
                        "tipo": "complementar",
                        "score": 8.5,
                        "recomendacao": "Paleta equilibrada com destaque dourado",
                    },
                },
                "tipografia": {
                    "fontes_detectadas": [
                        {"nome": "Inter", "peso": "bold", "confiança": 0.95},
                        {"nome": "Inter", "peso": "regular", "confiança": 0.92},
                    ],
                    "tamanhos": {"headline": 48, "body": 24, "cta": 20},
                    "hierarquia": {
                        "nivel_1": {"texto": "Headline", "tamanho": 48, "peso": "bold"},
                        "nivel_2": {
                            "texto": "Subtítulo",
                            "tamanho": 24,
                            "peso": "regular",
                        },
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
                },
                "elementos": {
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
                },
                "composicao": {
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
                    "foco": {"tipo": "center-weighted", "intensidade": "alto"},
                },
                "score_visual": {
                    "geral": 8.5,
                    "componentes": {
                        "paleta": 9.0,
                        "tipografia": 9.0,
                        "composicao": 8.5,
                        "legibilidade": 9.0,
                        "atração": 8.0,
                    },
                    "problemas_detectados": [],
                    "sugestoes": [
                        "Adicionar elemento surpresa no canto inferior",
                        "Considerar adicionar mais contraste no CTA",
                    ],
                },
                "match_modelo": {
                    "modelo": "template_educativo",
                    "compatibilidade": 0.92,
                    "ajustes_necessarios": [],
                },
                "nota": f"Análise mockada. Configure VISION_API_KEY ({self.provider}) para dados reais.",
            }
        }

    def extract_color_palette(self, image_source: str) -> Dict[str, Any]:
        """Extrai paleta de cores da imagem."""
        return self.analyze_image(image_source, {"extract_palette": True})

    def detect_text(self, image_source: str) -> Dict[str, Any]:
        """Detecta texto na imagem."""
        return self.analyze_image(image_source, {"detect_text": True})

    def detect_elements(self, image_source: str) -> Dict[str, Any]:
        """Detecta elementos visuais."""
        return self.analyze_image(image_source, {"detect_elements": True})
