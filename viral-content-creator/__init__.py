"""
Viral Content Creator - Skill de Criação de Conteúdo Viral

Analisa perfis, posts, copies, imagens e estilo para modelar e gerar conteúdo viral.

Criador: @monrars (Instagram)
Site: https://goldneuron.io/
Comunidade: https://goldneuron.io/drops
"""

__version__ = "1.0.0"
__author__ = "@monrars"

from .analyzer.profile_analyzer import ProfileAnalyzer
from .analyzer.post_analyzer import PostAnalyzer
from .analyzer.image_analyzer import ImageAnalyzer
from .models.style_model import StyleModeler
from .generator.content_generator import ContentGenerator
from .utils.dashboard import Dashboard

__all__ = [
    "ProfileAnalyzer",
    "PostAnalyzer",
    "ImageAnalyzer",
    "StyleModeler",
    "ContentGenerator",
    "Dashboard",
]
