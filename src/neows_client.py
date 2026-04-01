## 3. src/neows_client.py (NOWY - uniwersalne HTTP)
# repr(``python)
import json
from pathlib import Path
from typing import Any, Dict, Optional

import requests
import yaml


class NeoWsClient:
    def __init__(
        self, config_filename: str = "config.yaml"
    ) -> None:  # (self, config_path: str = "config/config.yaml"):
        # find config file relative to neows_client.py file
        module_dir = Path(__file__).parent  # katalog src/
        project_root = module_dir.parent  # katalog główny projektu
        config_path = project_root / "config" / config_filename

        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path) as f:
            self.config = yaml.safe_load(f)["api"]

        self.base_url = self.config["base_url"]
        self.api_key = self.config["api_key"]
        self.session = requests.Session()
        self.session.params = {"api_key": self.api_key}

    # Universal HTTP methods
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """GET for any endpoint"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        #
        print("request sent: ", url, params)
        #
        response = self.session.get(url, params=params or {})
        response.raise_for_status()
        return response.json()

    def post(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """POST request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.post(url, json=json_data, params=params or {})
        response.raise_for_status()
        return response.json()

    def put(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """PUT request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.put(url, json=json_data, params=params or {})
        response.raise_for_status()
        return response.json()

    def patch(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """PATCH request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.patch(url, json=json_data, params=params or {})
        response.raise_for_status()
        return response.json()

    # Specific NeoWs (get() is used)
    def get_feed(self, start_date: str, end_date: str = None) -> Dict[str, Any]:
        params = {"start_date": start_date}
        if end_date:
            params["end_date"] = end_date
        return self.get("feed", params=params)

    def get_browse(self, page: int = 0) -> Dict[str, Any]:
        return self.get("neo/browse", params={"page": page})

    def get_neo(self, neo_id: int) -> Dict[str, Any]:
        return self.get(f"neo/{neo_id}")

    def save_json_to_file(self, data: dict, filepath: str) -> None:
        """Saves (JSON) dictionary to a file"""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
