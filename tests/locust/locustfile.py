from typing import Optional

from locust import HttpUser
from locust import task

from tests.locust.request_factories.health_factory import HealthRequestFactory
from tests.locust.request_factories.users_factory import UsersRequestFactory


class APILoadTests(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.users_requests_factory = UsersRequestFactory(self.client)
        self.health_requests_factory = HealthRequestFactory(self.client)

    @task
    def health(self):
        self.health_requests_factory.get_health()

    @task
    def create_user(self):
        self.users_requests_factory.create_new_user()

    @task
    def create_and_get_user(self):
        new_user_id: Optional[int] = UsersRequestFactory(client=self.client).create_new_user()
        if new_user_id:
            self.users_requests_factory.get_user_by_id(new_user_id)

    @task
    def create_and_delete_user(self):
        new_user_id: Optional[int] = UsersRequestFactory(client=self.client).create_new_user()
        if new_user_id:
            self.users_requests_factory.delete_user_by_id(new_user_id)
