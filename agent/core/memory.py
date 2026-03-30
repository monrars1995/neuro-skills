"""
Sistema de Memória Compartilhada - Neuro Skills Agent
Autor: Monrars (@monrars)
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


class MemoryManager:
    """Gerenciador de memória compartilhada"""

    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.clients_dir = self.base_dir / "clients"
        self.shared_dir = self.base_dir / "shared"
        self.sessions_dir = self.base_dir / "sessions"

    def _read_json(self, path: Path) -> Dict[str, Any]:
        """Lê arquivo JSON"""
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _write_json(self, path: Path, data: Dict[str, Any]) -> bool:
        """Escreve arquivo JSON"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        return True

    def _get_timestamp(self) -> str:
        """Retorna timestamp atual"""
        return datetime.now().isoformat()

    # ========== CLIENTES ==========

    def list_clients(self) -> Dict[str, Any]:
        """Lista todos os clientes"""
        index_path = self.clients_dir / "index.json"
        return self._read_json(index_path)

    def get_client(self, client_id: str) -> Dict[str, Any]:
        """Obtém dados do cliente"""
        profile_path = self.clients_dir / client_id / "profile.json"
        return self._read_json(profile_path)

    def create_client(self, client_id: str, data: Dict[str, Any]) -> bool:
        """Cria novo cliente"""
        client_dir = self.clients_dir / client_id
        profile_path = client_dir / "profile.json"

        data["client_id"] = client_id
        data["created_at"] = self._get_timestamp()
        data["updated_at"] = self._get_timestamp()

        self._write_json(profile_path, data)

        # Atualizar índice
        index = self.list_clients()
        if "clients" not in index:
            index["clients"] = {}
        index["clients"][client_id] = {
            "name": data.get("name", client_id),
            "industry": data.get("industry", ""),
            "created_at": data["created_at"],
        }
        index["updated_at"] = self._get_timestamp()
        self._write_json(self.clients_dir / "index.json", index)

        return True

    def update_client(self, client_id: str, data: Dict[str, Any]) -> bool:
        """Atualiza dados do cliente"""
        profile_path = self.clients_dir / client_id / "profile.json"
        profile = self._read_json(profile_path)
        profile.update(data)
        profile["updated_at"] = self._get_timestamp()
        return self._write_json(profile_path, profile)

    def set_active_client(self, client_id: str) -> bool:
        """Define cliente ativo"""
        index = self.list_clients()
        index["active_client"] = client_id
        if client_id not in index.get("recent_clients", []):
            if "recent_clients" not in index:
                index["recent_clients"] = []
            index["recent_clients"].insert(0, client_id)
            index["recent_clients"] = index["recent_clients"][:5]  # Keep last 5
        return self._write_json(self.clients_dir / "index.json", index)

    def get_active_client(self) -> Optional[str]:
        """Retorna cliente ativo"""
        index = self.list_clients()
        return index.get("active_client")

    # ========== BRAND VOICE ==========

    def get_brand_voice(self, client_id: str) -> Dict[str, Any]:
        """Obtém voz da marca"""
        voice_path = self.clients_dir / client_id / "brand_voice.json"
        return self._read_json(voice_path)

    def save_brand_voice(self, client_id: str, voice_data: Dict[str, Any]) -> bool:
        """Salva voz da marca"""
        voice_path = self.clients_dir / client_id / "brand_voice.json"
        voice_data["updated_at"] = self._get_timestamp()
        if "created_at" not in voice_data:
            voice_data["created_at"] = self._get_timestamp()
        return self._write_json(voice_path, voice_data)

    # ========== META ACCOUNTS ==========

    def list_accounts(self) -> Dict[str, Any]:
        """Lista contas Meta"""
        accounts_path = self.shared_dir / "accounts.json"
        return self._read_json(accounts_path)

    def get_account(self, account_name: str) -> Optional[Dict[str, Any]]:
        """Obtém conta específica"""
        accounts = self.list_accounts()
        return accounts.get("accounts", {}).get(account_name)

    def save_account(self, account_name: str, account_data: Dict[str, Any]) -> bool:
        """Salva conta Meta"""
        accounts = self.list_accounts()
        if "accounts" not in accounts:
            accounts["accounts"] = {}
        accounts["accounts"][account_name] = account_data
        accounts["accounts"][account_name]["updated_at"] = self._get_timestamp()
        if "created_at" not in accounts["accounts"][account_name]:
            accounts["accounts"][account_name]["created_at"] = self._get_timestamp()
        return self._write_json(self.shared_dir / "accounts.json", accounts)

    def set_active_account(self, account_name: str) -> bool:
        """Define conta ativa"""
        accounts = self.list_accounts()
        accounts["active_account"] = account_name
        return self._write_json(self.shared_dir / "accounts.json", accounts)

    def get_active_account(self) -> Optional[str]:
        """Retorna conta ativa"""
        accounts = self.list_accounts()
        return accounts.get("active_account")

    # ========== CAMPAIGNS ==========

    def list_campaigns(self, client_id: str) -> Dict[str, Any]:
        """Lista campanhas do cliente"""
        history_path = self.clients_dir / client_id / "history.json"
        return self._read_json(history_path)

    def save_campaign(
        self, client_id: str, campaign_id: str, campaign_data: Dict[str, Any]
    ) -> bool:
        """Salva campanha"""
        history_path = self.clients_dir / client_id / "history.json"
        history = self._read_json(history_path)
        if "campaigns" not in history:
            history["campaigns"] = {}
        history["campaigns"][campaign_id] = campaign_data
        history["campaigns"][campaign_id]["updated_at"] = self._get_timestamp()
        return self._write_json(history_path, history)

    # ========== LEARNINGS ==========

    def get_learnings(self) -> Dict[str, Any]:
        """Obtém aprendizados globais"""
        learnings_path = self.shared_dir / "learnings.json"
        return self._read_json(learnings_path)

    def save_learning(self, category: str, key: str, value: Any) -> bool:
        """Salva aprendizado"""
        learnings = self.get_learnings()
        if category not in learnings:
            learnings[category] = {}
        learnings[category][key] = value
        learnings["updated_at"] = self._get_timestamp()
        return self._write_json(self.shared_dir / "learnings.json", learnings)

    # ========== PERFORMANCE ==========

    def get_performance(self, client_id: str) -> Dict[str, Any]:
        """Obtém performance do cliente"""
        perf_path = self.clients_dir / client_id / "performance.json"
        return self._read_json(perf_path)

    def update_performance(self, client_id: str, metrics: Dict[str, Any]) -> bool:
        """Atualiza métricas de performance"""
        perf_path = self.clients_dir / client_id / "performance.json"
        perf = self._read_json(perf_path)

        # Acumular métricas
        if "history" not in perf:
            perf["history"] = []
        perf["history"].append({"timestamp": self._get_timestamp(), **metrics})

        # Atualizar totais
        if "totals" not in perf:
            perf["totals"] = {}
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                perf["totals"][key] = perf["totals"].get(key, 0) + value

        perf["updated_at"] = self._get_timestamp()
        return self._write_json(perf_path, perf)
