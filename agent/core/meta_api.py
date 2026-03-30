"""
Meta Graph API Client - Neuro Skills Agent
Autor: Monrars (@monrars)
"""

import os
import time
import requests
from typing import Optional, Dict, Any, List, Callable
from pathlib import Path
from datetime import datetime


class MetaAPIClient:
    """Cliente para Meta Graph API v21.0"""

    def __init__(self, access_token: str, ad_account_id: str):
        self.access_token = access_token
        self.ad_account_id = (
            ad_account_id.replace("act_", "") if ad_account_id else None
        )
        self.base_url = "https://graph.facebook.com/v21.0"
        self.session = requests.Session()
        self.session.params = {"access_token": access_token}

    # ========== UPLOAD PROGRESS ==========

    def _upload_with_progress(
        self,
        file_path: Path,
        upload_url: str,
        progress_callback: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """Upload de arquivo com acompanhamento de progresso"""

        file_size = os.path.getsize(file_path)
        uploaded = 0

        def read_chunk(chunk_size=1024 * 1024):  # 1MB chunks
            nonlocal uploaded
            with open(file_path, "rb") as f:
                while True:
                    data = f.read(chunk_size)
                    if not data:
                        break
                    uploaded += len(data)
                    if progress_callback:
                        progress = uploaded / file_size
                        progress_callback(progress, uploaded, file_size)
                    yield data

        # Upload usando requests
        with open(file_path, "rb") as f:
            if progress_callback:
                # Simular progresso inicial
                progress_callback(0, 0, file_size)

            response = self.session.post(
                upload_url, files={"source": (file_path.name, f, "video/mp4")}
            )

            if progress_callback:
                # Progresso final
                progress_callback(1.0, file_size, file_size)

        return response.json()

    # ========== VIDEO UPLOAD ==========

    def upload_video(
        selfvideo_path: Path, progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Upload de vídeo para Meta Ads com acompanhamento de progresso

        Args:
            video_path: Caminho do arquivo de vídeo
            progress_callback: Função de callback para progresso(proportion, uploaded, total)

        Returns:
            Dict com video_id e status
        """
        url = f"{self.base_url}/{self.ad_account_id}/advideos"

        # Verificar tamanho do arquivo
        file_size_mb = os.path.getsize(video_path) / (1024 * 1024)

        if file_size_mb > 1000:  # Meta limit is 1GB
            return {
                "success": False,
                "error": f"Arquivo muito grande: {file_size_mb:.2f}MB. Limite: 1000MB",
            }

        # Upload com progresso
        if progress_callback:
            progress_callback(0.05, 0, os.path.getsize(video_path))

        try:
            with open(video_path, "rb") as video_file:
                files = {"source": (video_path.name, video_file, "video/mp4")}
                data = {
                    "title": video_path.stem,
                    "description": f"Video uploaded via Neuro Skills Agent",
                }

                # Upload em chunks para mostrar progresso
                response = self.session.post(
                    url,
                    files=files,
                    data=data,
                    timeout=3600,  # 1 hour timeout
                )

                if progress_callback:
                    progress_callback(
                        1.0, os.path.getsize(video_path), os.path.getsize(video_path)
                    )

                result = response.json()

                if "id" in result:
                    return {
                        "success": True,
                        "video_id": result["id"],
                        "file_size_mb": file_size_mb,
                        "filename": video_path.name,
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("error", {}).get(
                            "message", "Unknown error"
                        ),
                    }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_video_status(self, video_id: str) -> Dict[str, Any]:
        """Verifica status do upload de vídeo"""
        url = f"{self.base_url}/{video_id}"
        params = {"fields": "id,title,description,status,source,created_time"}

        response = self.session.get(url, params=params)
        return response.json()

    # ========== IMAGE UPLOAD ==========

    def upload_image(self, image_path: Path) -> Dict[str, Any]:
        """Upload de imagem para Meta Ads"""
        url = f"{self.base_url}/{self.ad_account_id}/adimages"

        file_size_mb = os.path.getsize(image_path) / (1024 * 1024)

        if file_size_mb > 30:  # Meta limit is 30MB
            return {
                "success": False,
                "error": f"Arquivo muito grande: {file_size_mb:.2f}MB. Limite: 30MB",
            }

        try:
            with open(image_path, "rb") as image_file:
                files = {"filename": (image_path.name, image_file, "image/jpeg")}

                response = self.session.post(url, files=files)
                result = response.json()

                if "images" in result:
                    return {
                        "success": True,
                        "image_hash": result["images"][image_path.name]["hash"],
                        "file_size_mb": file_size_mb,
                        "filename": image_path.name,
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("error", {}).get(
                            "message", "Unknown error"
                        ),
                    }

        except Exception as e:
            return {"success": False, "error": str(e)}

    # ========== CAMPAIGN CREATION ==========

    def create_campaign(
        self, name: str, objective: str, status: str = "PAUSED"
    ) -> Dict[str, Any]:
        """Cria campanha"""
        url = f"{self.base_url}/act_{self.ad_account_id}/campaigns"
        data = {
            "name": name,
            "objective": objective,
            "status": status,
            "special_ad_categories": "[]",
        }

        response = self.session.post(url, data=data)
        return response.json()

    def create_ad_set(
        self,
        campaign_id: str,
        name: str,
        daily_budget: int,
        targeting: Dict,
        optimization_goal: str = "CONVERSIONS",
        billing_event: str = "IMPRESSIONS",
        bid_amount: int = None,
    ) -> Dict[str, Any]:
        """Cria conjunto de anúncios"""
        url = f"{self.base_url}/act_{self.ad_account_id}/adsets"

        data = {
            "name": name,
            "campaign_id": campaign_id,
            "daily_budget": daily_budget,
            "targeting": targeting,
            "optimization_goal": optimization_goal,
            "billing_event": billing_event,
            "status": "PAUSED",
        }

        if bid_amount:
            data["bid_amount"] = bid_amount

        response = self.session.post(url, data=data)
        return response.json()

    def create_ad(self, ad_set_id: str, name: str, creative_id: str) -> Dict[str, Any]:
        """Cria anúncio"""
        url = f"{self.base_url}/act_{self.ad_account_id}/ads"
        data = {
            "name": name,
            "adset_id": ad_set_id,
            "creative": {"creative_id": creative_id},
            "status": "PAUSED",
        }

        response = self.session.post(url, data=data)
        return response.json()

    def create_ad_creative(
        self,
        name: str,
        page_id: str,
        video_id: str = None,
        image_hash: str = None,
        link: str = None,
        message: str = None,
        call_to_action: Dict = None,
    ) -> Dict[str, Any]:
        """Cria criativo de anúncio"""
        url = f"{self.base_url}/act_{self.ad_account_id}/adcreatives"

        # Montar objeto do criativo
        object_story_spec = {"page_id": page_id}

        if video_id:
            # Video creative
            object_story_spec["video_data"] = {
                "video_id": video_id,
                "title": name,
                "message": message or "",
            }
            if call_to_action:
                object_story_spec["video_data"]["call_to_action"] = call_to_action
            if link:
                object_story_spec["video_data"]["link"] = link
        elif image_hash:
            # Image creative
            object_story_spec["link_data"] = {
                "image_hash": image_hash,
                "link": link or "",
                "message": message or "",
            }
            if call_to_action:
                object_story_spec["link_data"]["call_to_action"] = call_to_action

        data = {"name": name, "object_story_spec": object_story_spec}

        response = self.session.post(url, data=data)
        return response.json()

    # ========== INSIGHTS ==========

    def get_campaign_insights(
        self, campaign_id: str, date_range: str = "last_7d"
    ) -> Dict[str, Any]:
        """Obtém insights da campanha"""
        url = f"{self.base_url}/{campaign_id}/insights"

        params = {
            "date_preset": date_range,
            "fields": "spend,impressions,clicks,cpc,ctr,cpm,reach,frequency,actions,cost_per_action_type",
        }

        response = self.session.get(url, params=params)
        return response.json()

    def get_ad_account_insights(self, date_range: str = "last_7d") -> Dict[str, Any]:
        """Obtém insights da conta"""
        url = f"{self.base_url}/act_{self.ad_account_id}/insights"

        params = {
            "date_preset": date_range,
            "fields": "spend,impressions,clicks,cpc,ctr,cpm,reach,frequency,actions,cost_per_action_type",
        }

        response = self.session.get(url, params=params)
        return response.json()

    # ========== UTILITY ==========

    def test_connection(self) -> Dict[str, Any]:
        """Testa conexão com a API"""
        try:
            url = f"{self.base_url}/me"
            response = self.session.get(url)
            data = response.json()
            return {
                "success": True,
                "user_id": data.get("id"),
                "user_name": data.get("name"),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_ad_account_info(self) -> Dict[str, Any]:
        """Obtém informações da conta de anúncios"""
        url = f"{self.base_url}/act_{self.ad_account_id}"
        params = {"fields": "id,name,currency,timezone_name,amount_spent,balance"}

        response = self.session.get(url, params=params)
        return response.json()
