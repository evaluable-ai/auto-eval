import requests
from evaluableai.data_model.model_response_object import ModelResponseObject
import uuid
import json
from requests.exceptions import RequestException
import time,os


class Mistral():
    def __init__(self, model_version, api_key_env):
        self._model_name = 'Mistral'
        self._model_version = model_version
        self._api_key_env = api_key_env
        self._response_list = None
        self._api_key = os.getenv(self._api_key_env)

    def __repr__(self):
        return (f"mistral(name={repr(self._model_name)}, "
                f"key={repr(self._api_key)}, "
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

    def generate_response(self, input_frame):

        response_list = []  # Initialize an empty list to hold response objects
        BASE_API_URL = "https://api-inference.huggingface.co/models/"
        API_URL = BASE_API_URL + self._model_version

        headers = {"Authorization": "Bearer " + self._api_key}

        max_retries = 3  # Maximum number of retries

        for input_row in input_frame:
            query = {
                "inputs": f"answer: {input_row.input_text} using the given context: {input_row.context}"
            }
            attempt = 0  # Current attempt number
            prompt = query['inputs']
            while attempt < max_retries:
                try:
                    response = requests.post(API_URL, headers=headers, json=query)
                    if response.status_code == 200:
                        response_data = response.json()
                        # Handle the case where the response is a list
                        if isinstance(response_data, list):
                            # Assuming the answer is in the first item of the list
                            response_json = response_data[0]
                            answer = response_json.get('generated_text', "The models did not return a valid answer.")
                            if answer.startswith(prompt):
                                answer = answer[len(prompt):].strip()
                        else:
                            answer = "Unexpected response format."
                        break
                    else:
                        print(f"Failed attempt {attempt + 1} with status code {response.status_code}")
                except RequestException as e:
                    print(f"Request failed: {e}")
                attempt += 1  # Increment the attempt counter

            if attempt == max_retries:
                # After all retries, if still not successful, raise an error
                raise Exception(f"Failed to get a valid response after {max_retries} attempts.")

            response_id = uuid.uuid4()
            # Create ModelResponseObject with the extracted answer
            model_response_object = ModelResponseObject(response_id, answer, input_row, self)
            response_list.append(model_response_object)

        self._response_list = response_list
        return response_list  # This should return the populated list
    