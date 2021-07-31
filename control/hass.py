from .config import resolve_config, Config

from requests import get, post
from typing import Dict


class HASS:
    def __init__(self, config: Config = None):
        self.config = resolve_config(config)

        self.headers = {
            "Authorization": "Bearer " + self.config.hass_auth_key.strip(),
            "content-type": "application/json",
        }

        self._base_url = "http://localhost:8123/api/"

    def _api(self, api: str) -> str:
        return self._base_url + api

    def _post(self, api: str, data: Dict) -> int:
        response = post(self._api(api), headers=self.headers, json=data)
        return response.status_code

    def toggle_light(self, entity: str) -> int:
        return self._post(api="services/light/toggle", data=dict(entity_id=entity))
