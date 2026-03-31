"""API integrations for viral-content-creator."""

from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

from .instagram_api import InstagramAPI
from .tiktok_api import TikTokAPI
from .twitter_api import TwitterAPI
from .vision_api import VisionAPI

__all__ = ["InstagramAPI", "TikTokAPI", "TwitterAPI", "VisionAPI"]
