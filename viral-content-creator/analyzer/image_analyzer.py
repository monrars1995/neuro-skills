"""Image analyzer backed by Vision API with safe fallback output."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, Optional


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.vision_api import VisionAPI


class ImageAnalyzer:
    BRAND_COLORS = {
        "primary": "#D4AF37",
        "secondary": "#000000",
        "background": "#0A0A0F",
        "text": "#FFFFFF",
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.cache: Dict[str, Dict[str, Any]] = {}
        self._vision = VisionAPI(
            api_key=self.config.get("vision_api_key"),
            provider=self.config.get("vision_provider", "google"),
        )

    def analyze(
        self, image_source: str, options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        options = options or {
            "extract_palette": True,
            "detect_text": True,
            "detect_elements": True,
            "analyze_composition": True,
            "score_visual": True,
        }
        result = self._vision.analyze_image(image_source, options)
        self.cache[image_source] = result
        return result

    def extract_palette_from_url(self, image_source: str) -> Dict[str, Any]:
        return self._vision.extract_color_palette(image_source)

    def detect_text(self, image_source: str) -> Dict[str, Any]:
        return self._vision.detect_text(image_source)

    def detect_elements(self, image_source: str) -> Dict[str, Any]:
        return self._vision.detect_elements(image_source)
