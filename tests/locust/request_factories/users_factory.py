from dataclasses import dataclass
from typing import Any
from typing import Dict

import ujson
from faker import Faker

from tests.locust.request_factories.base import BaseRequestFactory


class UsersRequestFactory(BaseRequestFactory):
    base_url: str = "/users"

    def get_user_by_id(self, user_id: int):
        self.client.get(f"{self.base_url}/{user_id}")

    def create_new_user(self) -> int:
        response = self.client.post(self.base_url, data=self._get_create_user_payload())
        return response.json().get("id")

    def delete_user_by_id(self, user_id: int):
        self.client.delete(f"{self.base_url}/{user_id}")

    @staticmethod
    def _get_create_user_payload() -> str:
        return ujson.dumps({"nickname": f"{Faker().word()}"})
