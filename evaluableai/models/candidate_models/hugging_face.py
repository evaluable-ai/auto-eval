import logging
import uuid

import requests
from requests.exceptions import RequestException

from evaluableai.data_model.model_response_object import ModelResponseObject

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class HuggingFace:
    BASE_API_URL = "https://api-inference.huggingface.co/models/"

    def __init__(self, model_version, api_key):
        self._model_name = 'hugging_face'
        self._model_version = model_version
        self._api_key = api_key
        self._response_list = None

    def __repr__(self):
        return (f"HuggingFace(name={repr(self._model_name)}, "
                f"version={repr(self._model_version)}, "
                f"api_key={repr(self._api_key)}, "
                f"response_list={repr(self._response_list)})")

    @property
    def model_name(self):
        return self._model_name

    @property
    def model_version(self):
        return self._model_version

    @property
    def api_key(self):
        return self._api_key

    @property
    def response_list(self):
        return self._response_list

    def _make_api_request(self, query):
        headers = {"Authorization": f"Bearer {self._api_key}"}
        API_URL = self.BASE_API_URL + self._model_version
        response = requests.post(API_URL, headers=headers, json=query)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()

    def generate_response(self, input_frame):
        self._response_list = []
        for input_row in input_frame:
            query = {
                "inputs": f"answer: {input_row.input_text} using the given context: {input_row.context}"
            }
            try:
                response_data = self._make_api_request(query)
                # Process the response
                if isinstance(response_data, list) and response_data:
                    answer = response_data[0].get('generated_text', "No valid answer returned.")
                else:
                    answer = "Unexpected response format."
            except RequestException as e:
                logging.error(f"Request failed: {e}")
                answer = "Failed to fetch response."
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                answer = "An error occurred while processing the request."

            response_id = uuid.uuid4()
            model_response_object = ModelResponseObject(response_id, answer, input_row, self)
            self._response_list.append(model_response_object)

        return self.response_list
