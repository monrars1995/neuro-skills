"""
Configuração do Neuro Skills Agent
Autor: Monrars (@monrars)
"""

import os
from pathlib import Path

# Diretório base da memória
NEURO_DIR = Path.home() / ".neuro-skills"

# Diretório de campanhas
CAMPAIGNS_DIR = Path("/campanhas")

# Diretório de uploads temporários
UPLOAD_TEMP_DIR = NEURO_DIR / "temp" / "uploads"

# Meta API Configuration
META_API_VERSION = "v21.0"
META_API_BASE = f"https://graph.facebook.com/{META_API_VERSION}"

# Limits
MAX_VIDEO_SIZE_MB = 1000  # Meta limit is 1GB
MAX_IMAGE_SIZE_MB = 30
UPLOAD_CHUNK_SIZE = 1024 * 1024 * 5  # 5MB chunks

# Supported formats
SUPPORTED_VIDEO_FORMATS = [".mp4", ".mov", ".avi", ".mkv"]
SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".gif"]

# Chunk size for progress tracking
PROGRESS_UPDATE_INTERVAL = 0.1  # Update progress every 10%# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Create directories
for dir_path in [NEURO_DIR, UPLOAD_TEMP_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


class Config:
    """Configuração dinâmica do agent"""

    def __init__(self):
        self.neuro_dir = NEURO_DIR
        self.campaigns_dir = CAMPAIGNS_DIR
        self.upload_temp_dir = UPLOAD_TEMP_DIR
        self.meta_api_version = META_API_VERSION
        self.meta_api_base = META_API_BASE

    def get_client_dir(self, client_id: str) -> Path:
        """Retorna diretório do cliente"""
        return self.neuro_dir / "clients" / client_id

    def get_campaign_dir(self, client_id: str, campaign_id: str) -> Path:
        """Retorna diretório da campanha"""
        return self.campaigns_dir / client_id / "campaigns" / campaign_id

    def get_session_file(self, skill_name: str) -> Path:
        """Retorna arquivo de sessão de um skill"""
        return self.neuro_dir / "sessions" / skill_name / "session.json"
