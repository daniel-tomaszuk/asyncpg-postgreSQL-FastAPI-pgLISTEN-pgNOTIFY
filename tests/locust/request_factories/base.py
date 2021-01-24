from locust.clients import HttpSession


class BaseRequestFactory:
    def __init__(self, client: HttpSession):
        self.client: HttpSession = client
