import logging
import uuid
import openai
from evaluableai.data_model.model_response_object import ModelResponseObject

class OpenAI:
    def __init__(self, model_version, api_key):
        self._model_name = 'open_ai'
        self._model_version = model_version
        self._api_key = api_key
        openai.api_key = self._api_key  # Set the API key for OpenAI

    @property
    def model_name(self):
        return self._model_name

    @property
    def model_version(self):
        return self._model_version

    @property
    def api_key(self):
        return self._api_key


    def _make_api_request(self, input_text, context):
        # Construct the prompt by combining context and input text
        prompt = f"{context}\n\n{input_text}"
        try:
            response = openai.Completion.create(
                engine=self._model_version,
                prompt=prompt,
                max_tokens=1000
            )
            return response
        except Exception as e:
            logging.error(f"An error occurred during API request: {e}")
            return None

    def generate_response(self, input_row):
        response_data = self._make_api_request(input_row.input_text, input_row.context)
        if response_data:
            answer = response_data.choices[0].text.strip()  # Updated to extract 'text'
        else:
            answer = "Failed to fetch response or an error occurred."
        response_id = str(uuid.uuid4())
        return ModelResponseObject(response_id, answer, input_row, self)

class OpenAiChat:
    def __init__(self, model_version, api_key):
        self._model_name = 'open_ai'
        self._model_version = model_version
        self._api_key = api_key
        self._response_list = None
        openai.api_key = self._api_key  # Set the API key for OpenAI

    @property
    def model_name(self):
        return self._model_name

    @property
    def model_version(self):
        return self._model_version

    @property
    def api_key(self):
        return self._api_key


    def _make_api_request(self, input_text, context):
        try:
            # Modify this part to use ChatCompletion for a conversation-based model
            response = openai.ChatCompletion.create(
                model=self._model_version,
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": input_text}
                ]
            )
            return response
        except Exception as e:
            logging.error(f"An error occurred during API request: {e}")
            return None

    def generate_response(self, input_row):
        self._response_list = []
        response_data = self._make_api_request(input_row.input_text, input_row.context)
        if response_data:
            answer = response_data.choices[0].message['content']
        else:
            answer = "Failed to fetch response or an error occurred."

        response_id = uuid.uuid4()
        return ModelResponseObject(response_id, answer, input_row, self)
