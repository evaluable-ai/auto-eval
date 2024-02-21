import requests
from .auth import Auth

class EvaluableAI:
    def __init__(self, token):
        self.auth = Auth(token)
        self.base_url = "https://api.evaluable.ai/auth/health"

    def make_request(self, method="GET", data=None):
        headers = self.auth.get_headers()
        url = f"{self.base_url}"
        response = requests.request(method, url, headers=headers, json=data)
        return response

    # Example method to interact with your API
    def get_resource(self, resource_id):
        endpoint = f"resources/{resource_id}"
        return self.make_request(endpoint)
