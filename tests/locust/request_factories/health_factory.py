from dataclasses import dataclass

from tests.locust.request_factories.base import BaseRequestFactory


class HealthRequestFactory(BaseRequestFactory):
    base_url: str = "/health"

    def get_health(self):
        self.client.get(f"{self.base_url}/")
