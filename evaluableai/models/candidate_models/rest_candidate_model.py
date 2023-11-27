import logging

import requests

from evaluableai.models.model import Model

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CustomModelClass(Model):
    """Custom model class for making requests to a REST API endpoint."""

    def __init__(self, model_name, model_version, api_endpoint, api_auth_token):
        """Initialize the custom model with an API endpoint and auth token."""
        self.model_name = model_name
        self.model_version = model_version
        self.api_endpoint = api_endpoint
        self.api_auth_token = api_auth_token
        self.headers = {'Authorization': f'Bearer {self.api_auth_token}'}

    def generate_response(self, input_frame):
        """Send a request to the API endpoint and return the response."""
        input_payload = [{
            "input_id": input_row.input_id,
            "input_text": input_row.input_text,
            "context": input_row.context
        } for input_row in input_rows]
        response = requests.post(
            self.api_endpoint,
            headers=self.headers,
            json={'input_json': input_payload}
        )
        response.raise_for_status()
        return response.json()
