"""
Módulo de Upload de Vídeos - Neuro Skills Agent
Autor: Monrars (@monrars)
"""

import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
import threading
from queue import Queue


class VideoUploadManager:
    """Gerenciador de uploads de vídeos com fila e progresso"""

    def __init__(self, api_client, max_concurrent: int = 3):
        """
        Inicializa gerenciador de uploads

        Args:
            api_client: Instância de MetaAPIClient
            max_concurrent: Máximo de uploads simultâneos
        """
        self.api_client = api_client
        self.max_concurrent = max_concurrent
        self.upload_queue = Queue()
        self.uploads = {}
        self.results = {}

    def add_to_queue(
        self,
        video_path: Path,
        creative_name: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Adiciona vídeo à fila de upload

        Args:
            video_path: Caminho do arquivo de vídeo
            creative_name: Nome do criativo
            metadata: Metadados adicionais

        Returns:
            ID do upload
        """
        upload_id = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{creative_name}"
        self.uploads[upload_id] = {
            "id": upload_id,
            "video_path": video_path,
            "creative_name": creative_name,
            "metadata": metadata or {},
            "status": "queued",
            "progress": 0,
            "uploaded_bytes": 0,
            "total_bytes": os.path.getsize(video_path),
            "error": None,
            "result": None,
            "started_at": None,
            "finished_at": None,
        }

        self.upload_queue.put(upload_id)
        return upload_id

    def _upload_worker(self, progress_callback: Optional[Callable] = None):
        """Worker de upload"""
        while True:
            upload_id = self.upload_queue.get()

            if upload_id is None:
                break

            upload = self.uploads[upload_id]
            upload["status"] = "uploading"
            upload["started_at"] = datetime.now().isoformat()

            # Callback de progresso interno
            def on_progress(proportion, uploaded, total):
                upload["progress"] = proportion
                upload["uploaded_bytes"] = uploaded
                if progress_callback:
                    progress_callback(upload_id, proportion, uploaded, total)

            # Upload
            result = self.api_client.upload_video(
                video_path=upload["video_path"], progress_callback=on_progress
            )

            # Atualizar status
            if result.get("success"):
                upload["status"] = "completed"
                upload["result"] = result
                upload["progress"] = 1.0
            else:
                upload["status"] = "failed"
                upload["error"] = result.get("error")

            upload["finished_at"] = datetime.now().isoformat()
            self.results[upload_id] = result

            self.upload_queue.task_done()

    def start_uploads(self, progress_callback: Optional[Callable] = None) -> None:
        """Inicia uploads em paralelo"""
        threads = []

        for _ in range(self.max_concurrent):
            thread = threading.Thread(
                target=self._upload_worker, args=(progress_callback,)
            )
            thread.daemon = True
            thread.start()
            threads.append(thread)

        return threads

    def wait_for_completion(self, timeout: int = 3600) -> Dict[str, Any]:
        """
        Aguarda todos os uploads finalizarem

        Args:
            timeout: Timeout em segundos

        Returns:
            Dict com resultados de todos os uploads
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            # Verificar se todos finalizaram
            all_done = True
            for upload in self.uploads.values():
                if upload["status"] in ["queued", "uploading"]:
                    all_done = False
                    break

            if all_done:
                break

            time.sleep(1)

        return self.results

    def get_status(self) -> Dict[str, Any]:
        """Retorna status de todos os uploads"""
        return {
            "total": len(self.uploads),
            "queued": sum(1 for u in self.uploads.values() if u["status"] == "queued"),
            "uploading": sum(
                1 for u in self.uploads.values() if u["status"] == "uploading"
            ),
            "completed": sum(
                1 for u in self.uploads.values() if u["status"] == "completed"
            ),
            "failed": sum(1 for u in self.uploads.values() if u["status"] == "failed"),
            "uploads": self.uploads,
        }

    def get_upload(self, upload_id: str) -> Optional[Dict[str, Any]]:
        """Retorna status de upload específico"""
        return self.uploads.get(upload_id)

    def cancel_upload(self, upload_id: str) -> bool:
        """Cancela upload (apenas se ainda na fila)"""
        if upload_id in self.uploads:
            upload = self.uploads[upload_id]
            if upload["status"] == "queued":
                upload["status"] = "cancelled"
                return True
        return False


class BatchUploader:
    """Upload de lote de criativos"""

    def __init__(self, api_client, memory_manager):
        self.api_client = api_client
        self.memory = memory_manager
        self.upload_manager = VideoUploadManager(api_client)

    def upload_creatives_from_folder(
        self,
        folder_path: Path,
        campaign_name: str,
        progress_callback: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """
        Upload de todos os criativos de uma pasta

        Args:
            folder_path: Caminho da pasta com criativos
            campaign_name: Nome da campanha
            progress_callback: Callback de progresso geral

        Returns:
            Dict com resultados dos uploads
        """
        results = {"videos": [], "images": [], "errors": []}

        # Encontrar arquivos
        video_extensions = [".mp4", ".mov", ".avi", ".mkv"]
        image_extensions = [".jpg", ".jpeg", ".png", ".gif"]

        files = list(folder_path.iterdir()) if folder_path.exists() else []

        # Separar vídeos e imagens
        videos = [f for f in files if f.suffix.lower() in video_extensions]
        images = [f for f in files if f.suffix.lower() in image_extensions]

        total_files = len(videos) + len(images)
        processed = 0

        # Upload de vídeos
        for video_path in videos:
            creative_name = video_path.stem

            # Adicionar à fila
            upload_id = self.upload_manager.add_to_queue(
                video_path=video_path,
                creative_name=creative_name,
                metadata={"campaign": campaign_name},
            )

            results["videos"].append(
                {"file": video_path.name, "upload_id": upload_id, "status": "queued"}
            )

        # Iniciar uploads
        threads = self.upload_manager.start_uploads(
            progress_callback=lambda uid, prog, up, total: (
                self._on_progress(uid, prog, up, total, results, progress_callback)
                if progress_callback
                else None
            )
        )

        # Upload de imagens (síncrono)
        for image_path in images:
            creative_name = image_path.stem

            result = self.api_client.upload_image(image_path)

            if result.get("success"):
                results["images"].append(
                    {
                        "file": image_path.name,
                        "hash": result["image_hash"],
                        "status": "completed",
                    }
                )
            else:
                results["errors"].append(
                    {
                        "file": image_path.name,
                        "type": "image",
                        "error": result.get("error"),
                    }
                )

            processed += 1
            if progress_callback:
                progress_callback(processed / total_files, processed, total_files)

        # Aguardar uploads de vídeo
        video_results = self.upload_manager.wait_for_completion()

        # Atualizar resultados
        for video_entry in results["videos"]:
            upload_id = video_entry["upload_id"]
            video_result = video_results.get(upload_id, {})

            if video_result.get("success"):
                video_entry["video_id"] = video_result["video_id"]
                video_entry["status"] = "completed"
            else:
                video_entry["status"] = "failed"
                video_entry["error"] = video_result.get("error")
                results["errors"].append(
                    {
                        "file": video_entry["file"],
                        "type": "video",
                        "error": video_result.get("error"),
                    }
                )

        return results

    def _on_progress(
        self,
        upload_id: str,
        proportion: float,
        uploaded: int,
        total: int,
        results: Dict,
        callback: Callable,
    ):
        """Callback interno de progresso"""
        for video in results["videos"]:
            if video["upload_id"] == upload_id:
                video["progress"] = proportion
                video["uploaded_bytes"] = uploaded
                break

        if callback:
            callback(proportion, uploaded, total)


class UploadProgressTracker:
    """Rastreador de progresso de upload"""

    def __init__(self):
        self.uploads = {}
        self.start_time = None

    def start(self):
        """Inicia tracker"""
        self.start_time = datetime.now()

    def update(self, upload_id: str, progress: float, uploaded: int, total: int):
        """Atualiza progresso"""
        self.uploads[upload_id] = {
            "progress": progress,
            "uploaded": uploaded,
            "total": total,
            "timestamp": datetime.now().isoformat(),
        }

    def get_overall_progress(self) -> float:
        """Retorna progresso geral"""
        if not self.uploads:
            return 0.0

        total_progress = sum(u["progress"] for u in self.uploads.values())
        return total_progress / len(self.uploads)

    def get_elapsed_time(self) -> float:
        """Retorna tempo decorrido em segundos"""
        if not self.start_time:
            return 0.0
        return (datetime.now() - self.start_time).total_seconds()

    def get_estimated_time_remaining(self) -> float:
        """Retorna tempo estimado restante em segundos"""
        progress = self.get_overall_progress()
        elapsed = self.get_elapsed_time()

        if progress <= 0:
            return 0.0

        rate = progress / elapsed
        remaining_progress = 1.0 - progress
        return remaining_progress / rate if rate > 0 else 0.0

    def format_progress(self) -> str:
        """Formata progresso para exibição"""
        progress = self.get_overall_progress()
        elapsed = self.get_elapsed_time()
        remaining = self.get_estimated_time_remaining()

        return f"Progresso: {progress * 100:.1f}% | Tempo: {elapsed:.0f}s | Restante: {remaining:.0f}s"
